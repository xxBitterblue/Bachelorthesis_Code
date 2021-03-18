<template>
    <div v-if="is_logged_in && user_role === Role.ADMIN">
        <h1>Validierungsregeln erstellen</h1>
        <div class="form-group">
            <input type="checkbox" class="form-check-input" id="validation_active" v-model="validation_rule.active">
            <label for="validation_active" class="form-check-label">Aktiv</label>
        </div>
        <div class="form-group">
            <input type="checkbox" class="form-check-input" id="validation_active_global" v-model="validation_rule.is_global">
            <label for="validation_active_global" class="form-check-label">Aktiv für alle Kategorien</label>
        </div>
        <Category-Tree v-if="!validation_rule.is_global"
            @last-category="last_category($event)"
        />
        <div class="form-group">
            <label class="form-text">Validierungsgruppe Name:</label>
            <input type="text" class="form-control" v-model="validation_rule.name">
        </div>
        <div class="row">
            <div class="col-6">
                <div class="form-group">    
                    <label class="form-text">Validierungsregel</label>
                    <textarea 
                    onkeydown="if(event.keyCode===9){var v=this.value,s=this.selectionStart,e=this.selectionEnd;this.value=v.substring(0, s)+'\t'+v.substring(e);this.selectionStart=this.selectionEnd=s+1;return false;}"
                    class="form-control rule" v-model="validation_rule.rule" />
                </div>
            </div>
            <div class="col-6">
                <fieldset disabled>
                    <label class="form-text">Validierungsregel Aufbau</label>
                    <p>
                        {{
                        software_structure
                        }}
                    </p>
                    <label class="form-text">Verfügbare Exceptions</label>
                    <div v-for="exception in exception_options" :key="exception">
                        {{
                        exception
                        }}
                    </div>
                </fieldset>
            </div>
        </div>
        <div class="col-4 mt-8">
            <button class="btn btn-primary mt-6" @click="save()">Speichern</button>
        </div>
        <div v-if="show_user_msg">
            <p>{{ user_mgs }}</p>
        </div>
    </div>
    <div v-else>
        <p>Um diese Seite zu sehen muss man eingeloggt sein und den Status Admin haben.</p>
        <router-link class="nav-link" to="/">Jetzt einloggen</router-link>
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, computed } from "vue"
import use_user from "../../composable/User"
import CategoryTree from "../req-group/Category-Tree.vue"
import * as Validation_APIHelper from "../../Helper/Validation_APIHelper"
import { CategoryModel } from "../../models/Category"
import { ValidationRuleModel } from "../../models/ValidationRule"
import { Role } from '../../Helper/enums'

    export default defineComponent ({
        name: "Update-Validation-Rule-Viewiew",

         props: {
            id: {type: Number, required: false}
        },

        components: {
            CategoryTree
        },

        setup(props) {
            const { user } = use_user()
            let is_logged_in = computed(() => user.value[`is_logged_in`])
            let user_role = computed(() => user.value[`role`])
            let show_user_msg = ref(false)
            let user_mgs = ref("")
            let software_structure = ref("")
            let exception_options = ref<string[]>([])
            let validation_rule = ref<ValidationRuleModel>({
                validation_rule_id: -1,
                name: "",
                active: true,
                is_global: false,
                rule: "",
                categorys: []
            })
 
            onMounted(async () => {
                if (props.id !== undefined) {
                    let rule = await Validation_APIHelper.get_rule(props.id)
                    validation_rule.value = rule
                }
                let validation_structure = await Validation_APIHelper.get_validation_structure()
                software_structure.value = JSON.stringify(validation_structure.software_structure, undefined, 4)
                exception_options.value = validation_structure.exception_options
            })

            function last_category(category: CategoryModel) {
                if (!validation_rule.value.is_global && validation_rule.value.categorys.find(ele => ele.category_id === category.category_id) === undefined) {
                    validation_rule.value.categorys.push(category)
                }
            }

            async function save() {
                if (validation_rule.value.validation_rule_id !== -1) {
                    if (validation_rule.value.name.trim() !== "" && validation_rule.value.rule !== "" && (validation_rule.value.categorys.length > 0 || validation_rule.value.is_global === true)) {
                        let result = await Validation_APIHelper.update_rule(validation_rule.value)
                        if (result === undefined) {
                           user_mgs.value = "Die Validierungsregel konnte nicht aktualisiert werden." 
                        } else {
                            user_mgs.value = "Die Validierungsregel konnte aktualisiert werden." 
                        }
                        show_user_msg.value = true
                   }
                } else {
                    let result = await Validation_APIHelper.add_rule(validation_rule.value)
                    if (result === undefined) {
                        user_mgs.value = "Die Validierungsregel konnte nicht hinzugefügt werden." 
                    } else {
                        user_mgs.value = "Die Validierungsregel konnte hinzugefügt werden." 
                    }
                    show_user_msg.value = true
                }
            }

            return {
                is_logged_in,
                validation_rule,
                last_category,
                save,
                software_structure,
                exception_options,
                user_role,
                Role,
                show_user_msg,
                user_mgs
            }
        }
    })
</script>

<style>
.rule{
    white-space: pre-wrap;
    overflow-wrap: normal;
}
</style>