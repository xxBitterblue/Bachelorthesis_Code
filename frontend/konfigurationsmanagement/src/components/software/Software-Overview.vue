<template>
    <div v-if="is_logged_in">
        <div class="row">
            <div clas="col-2 md-10">
                <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#softwareModal" v-on:click="open_modal(undefined)">
                    Hinzufügen
                </button>
            </div>
        </div>
        <div class="row">
            <!-- Modal -->
            <div v-if="show_modal">
                <transition name="softwareModal">
                    <div class="modal-mask">
                        <div class="modal-wrapper">
                            <div class="modal-dialog" role="document">
                                <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="softwareModalLabel">Software bearbeiten oder hinzufügen</h5>
                                    <button type="button" v-on:click="close_modal" class="btn close" data-bs-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                                <div class="modal-body">
                                    <div class="input-group mb-3">
                                        <div class="input-group-prepend">
                                            <span class="input-group-text">Name:</span>
                                        </div>
                                        <input type="text" class="form-control" v-model="update_software.name">
                                    </div>
                                    <div class="input-group mb-3">
                                        <div class="input-group-prepend">
                                            <span class="input-group-text">Version:</span>
                                        </div>
                                        <input type="text" class="form-control" v-model="update_software.version">
                                    </div>
                                    <div class="input-group mb-3">
                                        <div class="input-group-prepend">
                                            <span class="input-group-text">Type:</span>
                                        </div>
                                        <input type="text" class="form-control" v-model="update_software.type">
                                    </div>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" v-on:click="close_modal" data-bs-dismiss="modal">Schließen</button>
                                    <button type="button" class="btn btn-primary" v-on:click="save">Speichern</button>
                                </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>
            <div class="col-6 md-6">
                <h1>Software Übersicht</h1>
            </div>
            <div class="col-12">
                <Software-Table
                    :softwareList="all_software_list"
                    :editAllowed="true"
                    @delete-software="delete_software($event)"
                    @update-software="open_modal($event)"
                />
            </div>
        </div>
    </div>
    <div v-else>
        <p>Um diese Seite zu sehen muss man eingeloggt sein.</p>
        <router-link class="nav-link" to="/">Jetzt einloggen</router-link>
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, computed } from "vue"
import use_user from "../../composable/User"
import * as Software_APIHelper from "../../Helper/Software_APIHelper"
import { SoftwareModel } from "../../models/Software"
import SoftwareTable from "./Software-Table.vue"

    export default defineComponent ({
        name: "Software-Overview",

        components: {
            SoftwareTable
        },

        setup() {
            const { user } = use_user()
            let is_logged_in = computed(() => user.value[`is_logged_in`])
            let all_software_list = ref<SoftwareModel[]>([])
            let show_modal = ref(false)
            let update_software = ref<SoftwareModel>({
                software_id: -1,
                name: "",
                version: "",
                type: "",
                dependency_software: []
            })

            onMounted(async () => {
                all_software_list.value = await Software_APIHelper.get_all()
            })

            async function delete_software(id: Number) {
                let result = await Software_APIHelper.delete_software(id)
                if (result) {
                   all_software_list.value = await Software_APIHelper.get_all() 
                }                
            }

            function open_modal(software) {
                if(software !== undefined) {
                    update_software.value.software_id = software.software_id
                    update_software.value.name = software.name
                    update_software.value.version = software.version
                    update_software.value.type = software.type
                    update_software.value.dependency_software = software.dependency_software
                }else {
                    update_software.value.software_id = -1
                    update_software.value.name = ''
                    update_software.value.version = ''
                    update_software.value.type = ''
                    update_software.value.dependency_software = []
                }
                show_modal.value = true
            }

            function close_modal() {
                show_modal.value = false
            }

            async function save() {
                if (update_software.value.software_id > 0) {
                    let result_software = await Software_APIHelper.update_software(update_software.value as SoftwareModel)
                    if(result_software){
                        all_software_list.value = await Software_APIHelper.get_all()
                    }
                } else {
                    let result_software = await Software_APIHelper.add_software(update_software.value as SoftwareModel)
                    if (result_software) {
                        all_software_list.value = await Software_APIHelper.get_all()
                    }
                }

                update_software.value = {
                    software_id: -1,
                    name: "",
                    version: "",
                    type: "",
                    dependency_software: []
                }
                close_modal()
            }

            return {
                is_logged_in,
                all_software_list,
                delete_software,
                open_modal,
                close_modal,
                show_modal,
                save,
                update_software                
            }
        }
    })
</script>

<style>

.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, .5);
  display: table;
  transition: opacity .3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

</style>