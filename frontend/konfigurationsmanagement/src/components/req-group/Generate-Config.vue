<template>
    <div v-if="is_logged_in && user_role === Role.ADMIN">
        <div v-if="show_modal">
            <transition name="softwareModal">
                <div class="modal-mask">
                    <div class="modal-wrapper">
                        <div class="modal-dialog" role="document">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="softwareModalLabel">Generierung</h5>
                                    <button type="button" v-on:click="close_modal" class="btn close" data-bs-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                                <div class="modal-body">
                                    <p v-if="path">Generierung war erfolgreich. Konfigurationsdaten sind hier zu finden: {{ path }}</p>
                                    <p v-else>Generierung hat nicht funktioniert.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </transition>
        </div>
        <Category-Tree
            @last-category="last_category($event)"
        />
        <div class="col-6 mb-6">
            <div class="list-group"
                @dragover.prevent
                @drop.prevent="drop($event, current_groups)"
            >
                <p>Vorhandene Gruppen</p>
                <div class="list-group-item" v-for="group in current_groups" :key="group.requirement_group_id"
                    :draggable='true'
                    @dragstart="dragStart($event, group)"
                    @dragend="dragEnd($event, group, current_groups)"
                >
                    <p>{{ group.requirement_group_name }}</p>
                    <p>{{ group.author.username }}</p>
                    <button class="btn btn-sm btn-outline-secondary" @click="show_details(group.requirement_group_id)">Detailseite</button>
                </div>  
            </div>
        </div>
        <div class="col-6 mb-6">

            <div class="list-group"
                @dragover.prevent
                @drop.prevent="drop($event, choosen_groups)"
            >
                <p>Ausgewählte Gruppen</p>
                <div class="list-group-item" v-for="group in choosen_groups" :key="group.requirement_group_id"
                    :draggable='true'
                    @dragstart="dragStart($event, group)"
                    @dragend="dragEnd($event, group, choosen_groups)"
                >
                    <p>{{ group.requirement_group_name }}</p>
                    <p>{{ group.author.username }}</p>
                    <button class="btn btn-sm btn-outline-secondary" @click="show_details(group.requirement_group_id)">Detailseite</button>
                </div>
            </div>
        </div>
        <button class="btn btn-primary" @click="generate_config()">Generieren</button>
    </div>
    <div v-else>
        <p>Um diese Seite zu sehen muss man eingeloggt sein und den Status Admin haben.</p>
        <router-link class="nav-link" to="/">Jetzt einloggen</router-link>
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, computed } from "vue"
import use_user from "../../composable/User"
import { CategoryRequirementGroupModel } from "../../models/RequirementGroup"
import { CategoryModel } from "../../models/Category"
import * as Requirement_Group_APIHelper from "../../Helper/Requirement_Group_APIHelper"
import * as Generate_Config_APIHelper from "../../Helper/Generate_Config_APIHelper"
import CategoryTree from "./Category-Tree.vue"
import { Role } from '../../Helper/enums'
import router from "@/router"
import SoftwareTable from "../software/Software-Table.vue"

    export default defineComponent ({
        name: "Generate_Config",

        components: {
            CategoryTree
        },

        setup(props) {
            const { user } = use_user()
            let is_logged_in = computed(() => user.value[`is_logged_in`])
            let username = computed(() => user.value[`username`])
            let user_role = computed(() => user.value[`role`])
            let choosen_groups = ref<CategoryRequirementGroupModel[]>([])
            let current_groups = ref<CategoryRequirementGroupModel[]>([])
            let current_category = ref()
            let path = ref("")
            let show_modal = ref(false)
            
            async function last_category(Category: CategoryModel) {
                current_category.value = Category 

                let groups = await Requirement_Group_APIHelper.get_groups_by_category(current_category.value)
                current_groups.value = groups.category_requirement_group
            }

            async function generate_config() {
                path.value = await Generate_Config_APIHelper.generate_config(choosen_groups.value)
                show_modal.value = true
            }

            function show_details(id) {
                router.push({name: 'Group_Detail_Page', params: {id, is_category: "true"}})
            }

            function dragStart(e, group) {
                e.dataTransfer.dropEffect = "copy"
                e.dataTransfer.setData('group', JSON.stringify(group))
            }

            function dragEnd(e, group, old_list) {
                if(!(e.dataTransfer.dropEffect === 'none' && e.dataTransfer.effectAllowed === 'uninitialized')){
                    let group_idx = old_list.indexOf(group)
                    old_list.splice(group_idx, 1)
                }
            }

            function drop(e, group_list) {
                const group = JSON.parse(e.dataTransfer.getData('group'))
                group_list.push(group)
            }

            function close_modal() {
                show_modal.value = false
            }

            return {
                is_logged_in,
                username,
                user_role,
                current_groups,
                choosen_groups,
                last_category,
                generate_config,
                show_details,
                dragStart,
                dragEnd,
                drop,
                Role,
                path,
                show_modal,
                close_modal
            }
        }
    })
</script>