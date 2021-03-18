<template>
    <div v-if="is_logged_in && !edit_group || (user_role === Role.ADMIN || (update_req_group !== undefined && username === update_req_group.author.username))">
        <div v-if="show_modal">
            <transition name="softwareModal">
                <div class="modal-mask">
                    <div class="modal-wrapper">
                        <div class="modal-dialog" role="document">
                            <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="softwareModalLabel">Fehler bei der Validierung</h5>
                                <button type="button" v-on:click="close_modal" class="btn close" data-bs-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div class="modal-body">
                                <p>{{ validation_error }}</p>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
            </transition>
        </div>
        <h1>Anforderungsgruppe erstellen</h1>
        <div class="form-group">
            <input type="checkbox" class="form-check-input" id="validation_active" v-model="validation_active">
            <label for="validation_active" class="form-check-label">Immer validieren</label>
        </div>
        <div class="col-4 mb-2">
            <div class="form-group">
                <label class="form-text">Anforderungsgruppen Name:</label>
                <input type="text" class="form-control" v-model="update_req_group.requirement_group_name">
            </div>
        </div>
        <Category-Tree
            @last-category="last_category($event)"
        />
        <div class="col-2 mb-2" v-if="update_req_group.category">
            <div class="form-group">
                <label class="form-text" v-if="update_req_group.category">Ausgewählte Kategorie:</label>
                <input type="text" disabled class="form-control" v-model="update_req_group.category.category_name">
            </div>
        </div>
        <div class="col-12 mt-4">
            <Software-Table
                :softwareList="all_software_list"
                :changeInfoActive="false"
                :editAllowed="false"
                :dragAllowed="true"
            />
            <p>Ausgewählte Software:</p>
            <Software-Table
                :softwareList="update_req_group.software_list"
                :changeInfoActive="validation_active"
                :editAllowed="false"
                :dragAllowed="true"
                @software-changed="validate_current_software($event)"
            />
        </div>
        <div class="form-group">
            <input type="checkbox" class="form-check-input" id="status" v-model="update_req_group.status">
            <label for="status" class="form-check-label">Status</label>
        </div>
        <div v-if="!update_req_group.status">
            <div class="form-group">    
                <label for="status_comment" class="form-text">Grund für nicht fertigen Status</label>
                <textarea id="status_comment" class="form-control" v-model="update_req_group.status_comment" />
            </div>
        </div>
        <div v-if="edit_group">
            <div class="form-group">    
                <label for="edit_reason" class="form-text">Grund für Änderung angeben</label>
                <textarea id="edit_reason" class="form-control" v-model="edit_reason" />
            </div>
        </div>
        <button class="btn btn-primary mt-4" @click="save()">Speichern</button>
        <div v-if="show_user_msg">
            <p>{{ user_mgs }}</p>
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
import SoftwareTable from "../software/Software-Table.vue"
import CategoryTree from "./Category-Tree.vue"
import { SoftwareModel } from "../../models/Software"
import { CategoryModel } from "../../models/Category"
import { RequirementGroupModel } from "../../models/RequirementGroup"
import * as Software_APIHelper from "../../Helper/Software_APIHelper"
import * as Requirement_Group_APIHelper from "../../Helper/Requirement_Group_APIHelper"
import * as Validation_APIHelper from "../../Helper/Validation_APIHelper"
import { Role } from '../../Helper/enums'

    export default defineComponent ({
        name: "Add_Req_Group",

        props: {
            id: {type: String, required: false}
        },

        components: {
            SoftwareTable,
            CategoryTree
        },

        setup(props) {
            const { user } = use_user()
            let validation_active = ref(false)
            let is_logged_in = computed(() => user.value[`is_logged_in`])
            let username = computed(() => user.value[`username`])
            let user_role = computed(() => user.value[`role`])
            let all_software_list = ref<SoftwareModel[]>([])
            let edit_group = ref(false)    
            let edit_reason = ref("")
            let validation_error = ref("")
            let show_modal = ref(false)
            let show_user_msg = ref(false)
            let user_mgs = ref("")
            let update_req_group = ref<RequirementGroupModel>({
                requirement_group_id: -1,
                requirement_group_name: "",
                status: false,
                status_comment: "",
                software_list: []
            })

             onMounted(async () => {
                all_software_list.value = await Software_APIHelper.get_all()

                if (props.id !== undefined) {
                    update_req_group.value = await Requirement_Group_APIHelper.get_requirement_group(parseInt(props.id,10))
                    edit_group.value = true
                    all_software_list.value = all_software_list.value.filter(ele => update_req_group.value.software_list.find(ele2 => ele2.software_id === ele.software_id) === undefined)
                }
            })

            function last_category(Category: CategoryModel) {
                update_req_group.value.category = Category 
            }

            async function save() {
               if (update_req_group.value.category !== undefined && update_req_group.value.requirement_group_name.trim() !== "" && update_req_group.value.software_list.length > 0 ) {
                    if (!edit_group.value) {
                        let group = await Requirement_Group_APIHelper.add_requirement_group(update_req_group.value)
                        show_user_msg.value = true 
                        if (group === undefined) {
                           user_mgs.value = "Die Anforderungsgruppe konnte nicht hinzugefügt werden." 
                        } else {
                            user_mgs.value = "Die Anforderungsgruppe konnte hinzugefügt werden." 
                        }
                    } else {
                        if (edit_reason.value.trim() !== "" && props.id !== undefined) {
                            let group = await Requirement_Group_APIHelper.update_requirement_group(update_req_group.value, props.id, edit_reason.value)
                            show_user_msg.value = true 
                            if (group === undefined) {
                                user_mgs.value = "Die Anforderungsgruppe konnte nicht aktualisiert werden." 
                            } else {
                                user_mgs.value = "Die Anforderungsgruppe konnte aktualisiert werden." 
                            }
                        }
                    }
                }
            }

            async function validate_current_software() {
                let result = ""
                if (update_req_group.value.category === undefined) {
                    result = await Validation_APIHelper.validate(update_req_group.value.software_list)
                } else {
                    result = await Validation_APIHelper.validate(update_req_group.value.software_list, update_req_group.value.category)
                }
                
                if (result !== "") {
                    validation_error.value = result
                    show_modal.value = true
                }
            }

            function close_modal() {
                show_modal.value = false
            }

            return {
                validation_active,
                all_software_list,
                is_logged_in,
                username,
                user_role,
                Role,
                last_category,
                edit_group,
                edit_reason,
                save,
                validate_current_software,
                validation_error,
                show_modal,
                close_modal,
                update_req_group,
                show_user_msg,
                user_mgs
            }
        }
    })
</script>