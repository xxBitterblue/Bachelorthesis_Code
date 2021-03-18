<template>
    <div v-if="is_logged_in && group !== undefined">
        <div class="col-4 mb-8">
            <button v-if="user_role==Role.ADMIN || username==group.author.username" v-on:click="open_edit(group.requirement_group_id)"
                class="btn btn-primary"
            >
                Bearbeiten
            </button>
        </div>
        <div class="col-4 mb-8">
            <label>Gruppenname:</label>
            <p>{{ group.requirement_group_name }}</p>
        </div>
        <div class="col-4 mb-8">
            <label>Ersteller:</label>
            <p>{{ group.author.username }}</p>
        </div>
        <div class="col-4 mb-8">
            <label>Status:</label>
            <p>{{ group.status }}</p>
        </div>
        <div class="col-4 mb-8">
            <label>Statuskommentar:</label>
            <p>{{ group.status_comment }}</p>
        </div>
        <div class="col-4 mb-8">
            <label>Zeitpunkt der Erstellung:</label>
            <p>{{ group.timestamp }}</p>
        </div>
        <div class="col-4 mb-8">
            <label>Kategorie:</label>
            <p>{{ group.category.category_name }}</p>
        </div>
        <div class="col-4 mb-8" v-if="is_category === 'true'">
            <label>Referenzgruppen:</label>
            <ul v-if="group.reference_groups !== undefined">
                <li v-for="ele in group.reference_groups" :key="ele">
                    <router-link :to="'/group_details_overview/' + ele">RequirementGroup {{ele}}</router-link>
                </li>
            </ul>
            <p v-else>Keine Referenzgruppen</p>
        </div>

        <div class="col-12">
            <label>Software:</label>
            <Software-Table
                :softwareList="group.software_list"
                :editAllowed="false"
            />
        </div>
        <button class="btn btn-outline-secondary btn-sm mb-4" v-on:click="show_comments = !show_comments">
            <span v-if="show_comments">Kommentare ausblenden</span>
            <span v-if="!show_comments">Kommentare anzeigen</span>
        </button>
        <div class="col-6 mb-6 mt-6" v-if="show_comments">
            <div v-for="comment in group.user_comments" :key="comment.user_comment_id">
                <p>{{ comment.author.username }}</p>
                <p>{{ comment.timestamp }}</p>
                <p>{{ comment.comment_text }}</p>
            </div>
            <div>
                <div class="form-group">    
                    <label>Neuer Kommentar</label>
                    <textarea class="form-control" v-model="new_comment_text" />
                    <button class="btn btn-primary btn-sm" v-on:click="add_new_comment">
                        Senden
                    </button>
                </div>
            </div>
        </div>
        <div class="col-12 mt-2" v-if="group.change_history !== undefined && group.change_history.length > 0">
            <h1>Änderungsverlauf</h1>
            <table class="table table-striped table-sm">
                <thead>
                    <tr>
                        <th scope="col">Bearbeiter</th>
                        <th scope="col">Zeitpunkt</th>
                        <th scope="col">Änderungsgrund</th>
                        <th scope="col">Änderungen</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="history_entry in group.change_history" :key="history_entry.change_history_entry_id">
                        <td>{{ history_entry.author.username }}</td>
                        <td>{{ history_entry.timestamp }}</td>
                        <td v-if="history_entry.change_reason === undefined"></td>
                        <td v-if="history_entry.change_reason !== undefined">{{ history_entry.change_reason }}</td>
                        <td>{{ history_entry.changes }}</td>
                    </tr>
                </tbody>
            </table>
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
import { RequirementGroupModel, CategoryRequirementGroupModel } from "../../models/RequirementGroup"
import * as Requirement_Group_APIHelper from "../../Helper/Requirement_Group_APIHelper"
import { Role } from '../../Helper/enums'
import router from "@/router"
import SoftwareTable from "../software/Software-Table.vue"

    export default defineComponent ({
        name: "Group_Detail_Page",

        components: {
            SoftwareTable
        },

        props: {
            id: {type: String, required: true},
            is_category: {type: String, required: false, default:'false'}
        },

        setup(props) {
            const { user } = use_user()
            let is_logged_in = computed(() => user.value[`is_logged_in`])
            let username = computed(() => user.value[`username`])
            let user_role = computed(() => user.value[`role`])
            let group = ref<RequirementGroupModel | CategoryRequirementGroupModel>()
            let show_comments = ref(false)
            let new_comment_text = ref("")
            let is_category = ref()
            onMounted(async () => {            
                if (props.is_category === 'true') {
                    group.value = await Requirement_Group_APIHelper.get_category_requirement_group(parseInt(props.id,10))
                } else {
                    group.value = await Requirement_Group_APIHelper.get_requirement_group(parseInt(props.id,10))
                }  
            })

            function open_edit(id) {
                router.push(`/add_req_group/${id}`)
            }

            async function add_new_comment() {
                if (new_comment_text.value.trim() !== "") {
                    let result = await Requirement_Group_APIHelper.add_new_comment(props.id, new_comment_text.value)
                    group.value = await Requirement_Group_APIHelper.get_requirement_group(parseInt(props.id,10))
                    new_comment_text.value = ""
                }
            }

            return {
                is_logged_in,
                username,
                user_role,
                group,
                open_edit,
                Role,
                show_comments,
                new_comment_text,
                add_new_comment
            }
        }
    })
</script>