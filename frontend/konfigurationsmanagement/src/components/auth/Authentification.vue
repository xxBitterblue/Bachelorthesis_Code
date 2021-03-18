<template>
    <div>
        <label>Username:</label>
        <input type="text" required v-model="username"/>
        <label>Passwort:</label>
        <input type="password" required v-model="password"/>
        <button v-on:click="login">Login</button> 
        <button v-on:click="register">Registrieren</button> 
        <div v-if="user_msg">
            {{ user_msg }}
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue"
import * as AuthenticationApi from "../../Helper/authentication_APIHelper"
import router from "@/router"
import use_user from "../../composable/User"
import use_usersocket from "../../composable/UserSocket"
import { Role } from '../../Helper/enums'

    export default defineComponent ({
        name: "Authentification",

        setup() {
            const { setUserData } = use_user()
            const { setSocketData } = use_usersocket()
            let username = ref("")
            let password = ref("")
            let user_msg = ref("")

            async function login() {
                if (username.value != "" && password.value) {
                    const answer = await AuthenticationApi.login(username.value, password.value)

                    if (answer["token"]) {
                        const get_user_data = await AuthenticationApi.get_user_data(answer["token"])
                    
                        if (get_user_data["user_id"]) {
                            setUserData(get_user_data["user_id"], username.value, answer["token"], get_user_data["role"] as Role, get_user_data["socket_id"])
                            setSocketData(get_user_data["socket_id"])
                            router.push(`/req_group_overview`)
                        }
                    }
                }
            }

            async function register() {
                if (username.value != "" && password.value) {
                    const answer = await AuthenticationApi.register(username.value, password.value)
                    if (answer == true) {
                        user_msg.value = "Registrierung war erfolgreich"
                    } else {
                        user_msg.value = "Registrierung war nicht erfolgreich"
                    }
                }
            }

            return {
                username,
                password,
                login,
                register,
                user_msg
            }
        }
    })
</script>