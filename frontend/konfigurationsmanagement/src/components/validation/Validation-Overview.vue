<template>
    <div v-if="is_logged_in && user_role === Role.ADMIN">
        <button class="btn btn-primary mb-6" v-on:click="add_rule()">
            Neue Regel erstellen
        </button>
        <table class="table table-striped table-sm">
            <thead>
                <tr>
                    <th scope="col">Name</th>
                    <th scope="col">Ersteller</th>
                    <th scope="col">Aktiv</th>
                    <th scope="col">Für alle aktiv</th>
                    <th scope="col">Kategorien</th>
                    <th scope="col"></th>
                    <th scope="col"></th>
                </tr>
            </thead>
            <tbody>

            </tbody>
            <tr v-for="rule in validation_rules" :key="rule.validation_rule_id">
                <td>{{ rule.name }}</td>
                <td>{{ rule.author.username }}</td>
                <td>{{ rule.active }}</td>
                <td>{{ rule.is_global }}</td>
                <td>
                    <ul>
                        <li v-for="category in rule.categorys" :key="category.category_id">
                            {{ category.category_name }}
                        </li>
                    </ul>
                </td>
                <td>
                    <button class="btn btn-outline-secondary" v-on:click="delete_rule(rule.validation_rule_id)">
                        Löschen
                    </button>
                </td>
                <td>
                    <button class="btn btn-outline-secondary" v-on:click="update_rule(rule)">
                        Bearbeiten
                    </button>
                </td>
            </tr>
        </table>
    </div>
    <div v-else>
        <p>Um diese Seite zu sehen muss man eingeloggt sein und den Status Admin haben.</p>
        <router-link class="nav-link" to="/">Jetzt einloggen</router-link>
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, computed } from "vue"
import use_user from "../../composable/User"
import * as Validation_APIHelper from "../../Helper/Validation_APIHelper"
import { ValidationRuleModel } from "../../models/ValidationRule"
import router from "@/router"
import { Role } from '../../Helper/enums'

    export default defineComponent ({
        name: "Validation-Overview",

        setup() {
            const { user } = use_user()
            let is_logged_in = computed(() => user.value[`is_logged_in`])
            let user_role = computed(() => user.value[`role`])
            let validation_rules = ref<ValidationRuleModel[]>([])

            onMounted(async () => {
                validation_rules.value = await Validation_APIHelper.get_all()
            })

            async function delete_rule(id: Number) {
                let result = await Validation_APIHelper.delete_rule(id)
                if (result) {
                    validation_rules.value = await Validation_APIHelper.get_all()
                }
            }

            async function update_rule(rule: ValidationRuleModel) {
                router.push(`/update_validation_rule/${rule.validation_rule_id}`)
            }

            function add_rule() {
                router.push(`/update_validation_rule`)
            }

            return {
                is_logged_in ,
                validation_rules,
                delete_rule,
                update_rule,
                add_rule,
                user_role,
                Role
            }
        }
    })
</script>