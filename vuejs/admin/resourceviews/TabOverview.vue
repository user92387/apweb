<template>
    <div>
        <ResourceMenu
            :items="namedResources" />
        <ResourceLinkMenu
            :items="links" />
        <v-data-table
            class="data-table"
            :headers="summaryHeaders"
            :hide-default-header="true"
            :items="summary"
            :items-per-page="5"
          ></v-data-table>
    </div>
</template>
<script>

import ResourceMenu from '../ResourceMenu.vue'
import ResourceLinkMenu from '../ResourceLinkMenu.vue'
import {mapGetters} from 'vuex'

export default {

    props: {
        data: Object,
    },

    data() {
        return {
            summaryHeaders: [
                {
                    text: "Summary Information",
                    align: "left",
                    sortable: false,
                    value: "title",
                },
                {
                    text: "Value",
                    align: "left",
                    sortable: false,
                    value: "value",
                },
            ],
        }
    },

    components: {
        ResourceMenu,
        ResourceLinkMenu,
    },

    computed: {
        ...mapGetters([
            'description',
            'namedResources',
            'links',
        ]),
        summary() {
            return this.data.summary
        },
    },

}
</script>
<style lang="sass" scoped>

.description
    font-weight: bold

.data-table
    margin-top: 32px

</style>
