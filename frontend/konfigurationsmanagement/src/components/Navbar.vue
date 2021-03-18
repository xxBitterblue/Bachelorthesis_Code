<template>
    <div v-if="is_logged_in">
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
             <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/dashboard">Dashboard</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/software_overview">Software Übersicht</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/req_group_overview">Anforderungsgruppen Übersicht</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/add_req_group">Anforderungsgruppe erstellen</router-link>
                    </li>
                    <li v-if="admin" class="nav-item">
                        <router-link class="nav-link" to="/add_cat_req_group">Kategorie Anforderungsgruppe erstellen</router-link>
                    </li>
                    <li  v-if="admin" class="nav-item">
                        <router-link class="nav-link" to="/validation">Validierungsregeln</router-link>
                    </li>
                    <li v-if="admin" class="nav-item">
                        <router-link class="nav-link" to="/generate_config">Konfiguration generieren</router-link>
                    </li>
                    <li class="nav-item">
                        <button class="btn btn-sm btn-outline-secondary" @click="logout">Logout</button>
                    </li>
                </ul>
            </div>
        </nav>
    </div>    
</template>

<script lang="ts">
import bootstrap from 'bootstrap'
import { defineComponent, ref} from "vue"
import router from "@/router"
import use_user from  "../composable/User"
import { Role } from '../Helper/enums'
import { computed } from "vue";
import * as Authentication_APIHelper from "../Helper/authentication_APIHelper"

    export default defineComponent ({
        name: "Navbar",

        setup() {
            const { setUserData, user, login } = use_user()
            let is_logged_in = computed(() => user.value[`is_logged_in`])
            let user_role = computed(() => user.value[`role`])
            let admin = computed(() => {
                return user.value[`role`] === Role.ADMIN
            }) 

            async function logout() {
                let result = await Authentication_APIHelper.logout()
                if (result) {
                    setUserData("", "", "", Role.USER, "", false)
                    router.push(`/`)
                }
            }

            return {
                is_logged_in,
                user_role,
                admin,
                logout
            }
        }
    })
</script>