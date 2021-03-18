import { ref, computed } from "vue"
import { Role } from '../Helper/enums'

const user_data = ref({
    user_id: "",
    username: "",
    user_token: "",
    role: Role.USER,
    is_logged_in: false,
    socket_id: ""
})

export default function use_user() {
    const user = computed(() => user_data.value)
    const login = ref(false)
    function setUserData(id: string, username: string, token: string, role: Role, socket_id: string, is_logged_in: boolean = true) {
        user_data.value["user_id"] = id
        user_data.value["username"] = username
        user_data.value["user_token"] = token
        user_data.value["role"] = role
        user_data.value["is_logged_in"] = is_logged_in
        user_data.value["socket_id"] = socket_id
        localStorage.setItem("user_token", token)
        login.value = true
    }

    return {
        setUserData, user, login
    }
}
