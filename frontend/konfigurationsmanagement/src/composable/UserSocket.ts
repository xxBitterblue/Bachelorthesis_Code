import { ref, computed } from "vue"

const socket_data = ref({
    socket_id: "",
    socket: null as any
})

export default function use_usersocket() {
    const socket_prefix = 'ws://localhost:8080/ws'
    const socket = computed(() => socket_data.value)
    function setSocketData(id) {
        socket_data.value["socket_id"] = id
        socket_data.value["socket"] = new WebSocket(socket_prefix + id)
    }

    return {
        socket,
        setSocketData
    }
}