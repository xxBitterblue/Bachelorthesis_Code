<template>
<div class="container">
  <div aria-live="polite" aria-atomic="true" style="position: relative; min-height: 200px;">
    <div v-if="toast_active" style="position: absolute; top: 0; right: 0; z-index: 1000;">
      <div data-bs-delay="10000" data-bs-autohide="true" :class="{toast: true, show: toast_active}" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
          <strong v-if="toasts.length === 1" class="mr-auto">{{current_toast.editor.username}}</strong>
          <button type="button" class="btn close" @click="close_toast()" data-bs-dismiss="toast" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div v-if="toasts.length === 1" class="toast-body" @click="to_group(current_toast.type_id)">
          {{current_toast.message}}
        </div>
        <div v-else class="toast-body" @click="to_dashboard()">
          Mehrere Neuigkeiten, gehen Sie zum Dashboard.
        </div>
      </div>
    </div>
    <Navbar></Navbar>
    <router-view/>
  </div>
</div>
</template>

<script type="ts">
  import Navbar from './components/Navbar'
  import { defineComponent, onMounted, watch, ref, computed} from "vue"
  import * as AuthenticationApi from "./Helper/authentication_APIHelper"
  import router from "@/router"
  import use_user from "./composable/User"
  import use_usersocket from "./composable/UserSocket"
  import { Role } from './Helper/enums'
  import { DashBoardModel } from "./models/Dashboard"
  export default defineComponent({

    components:{
      Navbar
    },

    setup(){
      const { user, setUserData, login } = use_user()  
      const { socket, setSocketData } = use_usersocket()
      let toasts = ref([])
      let toast_active = ref(false)
      let current_toast = computed(() => toasts.value[toasts.value.length - 1])
      watch(login, (oldVal, newVal) => {
        let loggedIn = login.value
        socket.value["socket"].onmessage = handleMsg
      })
      
      onMounted(async () => {
          const token = localStorage.getItem("user_token")
          if(token !== undefined && token !== null){
              const get_user_data = await AuthenticationApi.get_user_data(token)
              if (get_user_data["user_id"]) {
                  setUserData(get_user_data["user_id"], get_user_data["username"], token, get_user_data["role"], get_user_data["socket_id"])
                  setSocketData(get_user_data["socket_id"])
                  socket.value["socket"].onmessage = handleMsg
                  router.push("/req_group_overview")
              }
          }
        }
      )

      function to_group(id){
          close_toast()
          router.push({name: 'Group_Detail_Page', params: {id, is_category: false}})
      }

      function to_dashboard(){
        close_toast()
        router.push(`/dashboard`)
      }

      function handleMsg(e) {
        const data = JSON.parse(e.data)
        if(data.type === 'new_changes'){
          toasts.value.push(data.message)
          toast_active.value = true
          setTimeout(() => {
            close_toast()
          }, 10000)
        }
      }

      function close_toast(){
        toasts.value = []
        toast_active.value = false
      }
      
      return {
        current_toast,
        to_group,
        to_dashboard,
        close_toast,
        toast_active,
        toasts
      }
    }
  })
</script>