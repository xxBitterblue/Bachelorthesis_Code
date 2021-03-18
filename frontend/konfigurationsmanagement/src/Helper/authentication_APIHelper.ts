import * as statics from "./statics"
import use_user from "../composable/User"

const { user } = use_user()

export function login(username: String, password: String) {
    return fetch(`${statics.auth_path}login/`, {
        method: "post",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "username": username,
            "password": password
        })
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        })
        .catch(reason => {
            return `Failed: ${reason}`
        })
}

export function logout() {
    return fetch(`${statics.auth_path}logout/`, {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        }
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return true
        })
        .catch(reason => {
            return `Failed: ${reason}`
        })
}

export function register(username: String, password: String) {
    return fetch(`${statics.auth_path}register/`, {
        method: "post",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "username": username,
            "password": password
        })
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return true
        })
        .catch(reason => {
            return `Failed: ${reason}`
        })
}

export function get_user_data(token: String) {
    return fetch(`${statics.auth_path}userdata/`, {
        method: "get",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + token
        }
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        })
        .catch(reason => {
            return `Failed: ${reason}`
        })
}