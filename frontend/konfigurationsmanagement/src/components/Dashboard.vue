<template>
    <div v-if="is_logged_in">
        <table class="table table-striped table-sm">
            <thead>
                <tr>
                    <th scope="col">Author</th>
                    <th scope="col">Datum</th>
                    <th scope="col">Nachricht</th>
                    <th scope="col"></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="dashboard_message in dashboard_list" :key="dashboard_message.dashboard_entry_id">
                    <td>{{dashboard_message.editor.username}}</td>
                    <td>{{dashboard_message.timestamp}}</td>
                    <td>{{dashboard_message.message}}</td>
                    <td>
                        <button class="btn btn-outline-secondary" @click="to_group(dashboard_message.type_id)">Details</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <div v-else>
        <p>Um diese Seite zu sehen muss man eingeloggt sein.</p>
        <router-link class="nav-link" to="/">Jetzt einloggen</router-link>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from "vue"
import { DashboardModel } from "../models/Dashboard"
import use_user from "../composable/User"
import router from "@/router"
import * as Requirement_Group_APIHelper from "../Helper/Requirement_Group_APIHelper"

    export default defineComponent ({
        name: "Dashboard",
        setup() {
            const { user } = use_user()
            let is_logged_in = computed(() => user.value[`is_logged_in`])
            let user_id = computed(() => user.value[`user_id`])
            let dashboard_list = ref<DashboardModel[]>([])

            onMounted(async () => {
                dashboard_list.value = await Requirement_Group_APIHelper.get_dashboard(user_id.value)
            })

            function to_group(id){
                router.push({name: 'Group_Detail_Page', params: {id, is_category: false as any}})
            }

            return {
                dashboard_list,
                is_logged_in,
                to_group
            }
        }
    })
</script>