import * as statics from "./statics"
import use_user from "../composable/User"
import { ValidationRuleModel, ValidationStructureModel } from "../models/ValidationRule"
import { SoftwareModel } from '@/models/Software';
import { CategoryModel } from '@/models/Category';

const { user } = use_user()

export function get_all(): Promise<ValidationRuleModel[]> {
    return fetch(`${statics.validation_path}`, {
        method: "get",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        }
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        }).then((data: { validation_rules: ValidationRuleModel[] }) => data.validation_rules)
}

export function get_rule(id: Number): Promise<ValidationRuleModel> {
    return fetch(`${statics.validation_path}${id}/`, {
        method: "get",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        }
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        }).then((data: { validation_rule: ValidationRuleModel }) => data.validation_rule)
}

export function delete_rule(id: Number): Promise<Boolean> {
    return fetch(`${statics.validation_path}delete/${id}/`, {
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
            return respo.json()
        }).then((data: Boolean) => data)
}

export function add_rule(validation_rule: ValidationRuleModel): Promise<ValidationRuleModel> {
    return fetch(`${statics.validation_path}add/`, {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        },
        body: JSON.stringify(validation_rule)
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        }).then((rule: ValidationRuleModel) => rule)
}

export function update_rule(validation_rule: ValidationRuleModel): Promise<ValidationRuleModel> {
    return fetch(`${statics.validation_path}update/${validation_rule.validation_rule_id}/`, {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        },
        body: JSON.stringify(validation_rule)
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        }).then((rule: ValidationRuleModel) => rule)
}

export function validate(software_list: SoftwareModel[], category?: CategoryModel): Promise<string> {
    let body_json = ""
    if (category !== undefined) {
        body_json = JSON.stringify({ "software_list": software_list, "category": category })
    } else {
        body_json = JSON.stringify({ "software_list": software_list })
    }
    return fetch(`${statics.validation_path}validate_group/`, {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        },
        body: body_json
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        }).then((data: { 'detail': string }) => data.detail)
}

export function get_validation_structure(): Promise<ValidationStructureModel> {
    return fetch(`${statics.validation_path}validation_structure/`, {
        method: "get",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        }
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        })
}