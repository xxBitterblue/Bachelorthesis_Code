<template>
    <div v-if="is_logged_in">
        <Category-Tree
            @last-category="reload_by_category($event)"
        />
        <table class="table table-striped table-sm">
            <thead>
                <tr>
                    <th scope="col">Name</th>
                    <th scope="col">Ersteller</th>
                    <th scope="col">Kategorie</th>
                    <th scope="col">Ist Kategorie Gruppe</th>
                    <th scope="col"></th>
                    <th scope="col"></th>
                    <th scope="col"></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="group in groups_list" :key="group.requirement_group_id">
                    <td>{{ group.requirement_group_name }}</td>
                    <td>{{ group.author.name }}</td>
                    <td>{{ group.category.category_name }}</td>
                    <td v-if="group.reference_groups !== undefined">ja</td>
                    <td v-else>nein</td>
                    <td>
                        <button class="btn btn-outline-secondary btn-sm" v-if="user_role==Role.ADMIN || username==group.author.username" v-on:click="delete_group(group.requirement_group_id)">
                            Löschen
                        </button>
                    </td>
                    <td>
                        <button class="btn btn-outline-secondary btn-sm" v-if="user_role==Role.ADMIN || username==group.author.username" v-on:click="open_edit(group)">
                            Bearbeiten
                        </button>
                    </td>
                    <td>
                        <button class="btn btn-outline-secondary btn-sm" v-on:click="open_details(group)">
                            Detailseite
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
            
        <ul>
            <li v-for="user in required_users" :key="user.user_id">
                {{ user.username }}
            </li>
        </ul>
    </div>
    <div v-else>
        <p>Um diese Seite zu sehen muss man eingeloggt sein.</p>
        <router-link class="nav-link" to="/">Jetzt einloggen</router-link>
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, computed } from "vue"
import use_user from "../../composable/User"
import CategoryTree from "./Category-Tree.vue"
import { CategoryModel } from "../../models/Category"
import { UserModel } from "../../models/User"
import { RequirementGroupModel, CategoryRequirementGroupModel } from "../../models/RequirementGroup"
import * as Requirement_Group_APIHelper from "../../Helper/Requirement_Group_APIHelper"
import router from "@/router"
import { Role } from '../../Helper/enums'

    export default defineComponent ({
        name: "Group_Overview",

        components: {
            CategoryTree
        },

        setup() {
            const { user } = use_user()
            let is_logged_in = computed(() => user.value[`is_logged_in`])
            let username = computed(() => user.value[`username`])
            let user_role = computed(() => user.value[`role`])
            let groups_list = ref<RequirementGroupModel[]>([])
            let required_users = ref<UserModel[]>([])

            onMounted(async () => {
                groups_list.value = await Requirement_Group_APIHelper.get_all_requirement_groups()
                let category_group = await Requirement_Group_APIHelper.get_all_category_requirement_groups()
                groups_list.value.push(...category_group)
            })

            async function reload_by_category(category: CategoryModel) {
                let groups = await Requirement_Group_APIHelper.get_groups_by_category(category)
                groups_list.value = groups.requirement_group
                groups_list.value.push(...groups.category_requirement_group)
                required_users.value = await Requirement_Group_APIHelper.get_required_users_by_category(category)
            }

            async function delete_group(id: Number) {
                let result = await Requirement_Group_APIHelper.delete_requirement_group(id)
                if (result) {
                    groups_list.value = await Requirement_Group_APIHelper.get_all_requirement_groups()
                }
            }

            function open_details(group: RequirementGroupModel | CategoryRequirementGroupModel) { 
                if(group.requirement_group_id !== undefined){
                    let id = group.requirement_group_id.toString()
                    let is_category = ((group as CategoryRequirementGroupModel).reference_groups !== undefined)
                    router.push({name: 'Group_Detail_Page', params: {id, is_category: is_category as any}})
                }
            }
            
            function open_edit(group: RequirementGroupModel | CategoryRequirementGroupModel) {
                if(group.requirement_group_id !== undefined){
                    let id = group.requirement_group_id.toString()
                    let is_category = ((group as CategoryRequirementGroupModel).reference_groups !== undefined)

                    if ((group as CategoryRequirementGroupModel).reference_groups !== undefined) {
                        router.push({name: 'Edit_Cat_Req_Group', params: {id}})
                    } else {
                        router.push({name: 'Edit_Req_Group', params: {id}})
                    }
                }
            }

            return {
                is_logged_in,
                username,
                user_role,
                groups_list,
                reload_by_category,
                delete_group,
                open_details,
                open_edit,
                Role,
                required_users
            }
        }
    })
</script>