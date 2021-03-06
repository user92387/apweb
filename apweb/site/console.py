# -*- coding:utf-8 -*-


def add_user(cmd_context):
    """Add a user to the database"""
    site = cmd_context.site
    args = cmd_context.args

    user_email = args.user_email
    password = args.password
    initiate_password_reset = args.initiate_password_reset
    roles = args.roles

    site.transaction_manager.begin()
    user = site["users"].add(user_email=user_email)
    if password:
        user.set_password(password)
    if initiate_password_reset:
        user.initiate_password_reset()
    if roles:
        for role in roles:
            user.assign_role(role)
    site.transaction_manager.commit()

    return 0


def assign_role(cmd_context):
    """Assign a role to a user"""
    site = cmd_context.site
    args = cmd_context.args

    user_email_or_uuid = args.user
    role = args.role

    site.transaction_manager.begin()
    user = None
    try:
        user = site['users'][user_email_or_uuid]
    except KeyError as e:
        user = site['users'].get_user_by_email(user_email_or_uuid)
        if user is None:
            raise Exception("user not found") from e

    role = role.strip()
    assert role
    user.assign_role(role)
    site.transaction_manager.commit()


def cmd_configure(sub_commands):
    """Configure arg parser commands related to apweb site"""

    # Add user command
    add_user_parser = sub_commands.add_parser(
        "add-user", help="Add a user to the database"
    )
    add_user_parser.add_argument(
        "user_email", help="the email used to authenticate the user"
    )
    add_user_parser.add_argument(
        "-i",
        "--initiate-password-reset",
        action="store_true",
        help="immediately send password reset email",
    )
    add_user_parser.add_argument(
        "-p",
        "--password",
        default=None,
        help="set password for password authenticateion",
    )
    add_user_parser.add_argument(
        "-r", "--role", action="append", dest="roles", help="assign roles to the user"
    )
    add_user_parser.set_defaults(func=add_user)

    # Assign role command
    assign_role_parser = sub_commands.add_parser(
        "assign-role", help="Assign a role to a user"
    )
    assign_role_parser.add_argument(
        "user", help="The user_uuid or email"
    )
    assign_role_parser.add_argument(
        "role", help="Trole to assign the user"
    )
    assign_role_parser.set_defaults(func=assign_role)
