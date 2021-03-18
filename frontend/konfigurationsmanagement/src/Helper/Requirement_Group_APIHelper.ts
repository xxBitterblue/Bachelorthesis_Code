import * as statics from "./statics"
import use_user from "../composable/User"
import { CategoryModel } from "../models/Category"
import { RequirementGroupModel, CategoryRequirementGroupModel } from "../models/RequirementGroup"
import { UserModel } from '@/models/User';
import { DashboardModel } from '@/models/Dashboard';

const { user } = use_user()

export function get_categorys(): Promise<CategoryModel[]> {
    return fetch(`${statics.base_path}categorys/ `, {
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
        }).then((data: { categorys: CategoryModel[] }) => data.categorys)
}

export function get_required_users_by_category(category: CategoryModel): Promise<UserModel[]> {
    return fetch(`${statics.base_path}categorys/${category.category_id}/get_required_users/ `, {
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
        }).then((data: { user_list: UserModel[] }) => data.user_list)
}

export function get_all_requirement_groups(): Promise<RequirementGroupModel[]> {
    return fetch(`${statics.requirement_group_path}`, {
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
        }).then((data: { requirement_groups: RequirementGroupModel[] }) => data.requirement_groups)
}

export function get_requirement_group(id: Number): Promise<RequirementGroupModel> {
    return fetch(`${statics.requirement_group_path}${id}/`, {
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
        }).then((data: { requirement_group: RequirementGroupModel }) => data.requirement_group)
}

export function get_all_category_requirement_groups(): Promise<CategoryRequirementGroupModel[]> {
    return fetch(`${statics.requirement_category_group_path}`, {
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
        }).then((data: { requirement_groups: CategoryRequirementGroupModel[] }) => data.requirement_groups)
}

export function get_category_requirement_group(id: Number): Promise<CategoryRequirementGroupModel> {
    return fetch(`${statics.requirement_category_group_path}${id}/`, {
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
        }).then((data: { requirement_groups: CategoryRequirementGroupModel }) => data.requirement_groups)
}

export function get_groups_by_category(category: CategoryModel): Promise<{ requirement_group: RequirementGroupModel[], category_requirement_group: CategoryRequirementGroupModel[] }> {
    return fetch(`${statics.requirement_group_path}category/${category.category_id}/`, {
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
        }).then((data: { requirement_group: RequirementGroupModel[], category_requirement_group: CategoryRequirementGroupModel[] }) => data)
}

export function add_requirement_group(requirement_group: RequirementGroupModel): Promise<RequirementGroupModel> {
    return fetch(`${statics.requirement_group_path}add/`, {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        },
        body: JSON.stringify(requirement_group)
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        }).then((data: RequirementGroupModel) => data)
}

export function update_requirement_group(requirement_group: RequirementGroupModel, id: string, edit_reason: string): Promise<RequirementGroupModel> {
    let json_body = JSON.stringify(requirement_group)
    let json = JSON.parse(json_body)
    json["change_reason"] = edit_reason
    return fetch(`${statics.requirement_group_path}update/${id}/`, {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        },
        body: JSON.stringify(json)
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        }).then((data: RequirementGroupModel) => data)
}

export function add_cat_requirement_group(requirement_group: CategoryRequirementGroupModel): Promise<CategoryRequirementGroupModel> {
    return fetch(`${statics.requirement_category_group_path}add/`, {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        },
        body: JSON.stringify(requirement_group)
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        }).then((data: CategoryRequirementGroupModel) => data)
}

export function update_cat_requirement_group(requirement_group: CategoryRequirementGroupModel, id: string, edit_reason: string): Promise<CategoryRequirementGroupModel> {
    let json_body = JSON.stringify(requirement_group)
    let json = JSON.parse(json_body)
    json["change_reason"] = edit_reason
    return fetch(`${statics.requirement_category_group_path}update/${id}/`, {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        },
        body: JSON.stringify(json)
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        }).then((data: CategoryRequirementGroupModel) => data)
}

export function delete_requirement_group(id: Number): Promise<Boolean> {
    return fetch(`${statics.requirement_group_path}delete/${id}/`, {
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

export function add_new_comment(id: string, comment_text: string): Promise<Boolean> {
    return fetch(`${statics.requirement_group_path}${id}/add_comment/`, {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        },
        body: JSON.stringify({ "comment_text": comment_text })
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        }).then((data: Boolean) => data)
}

export function get_dashboard(id: string): Promise<DashboardModel[]> {
    return fetch(`${statics.base_path}dashboard/${id}/`, {
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
        }).then((data: { dashboard: DashboardModel[] }) => data.dashboard)
}