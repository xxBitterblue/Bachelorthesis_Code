import * as statics from "./statics"
import use_user from "../composable/User"
import { CategoryRequirementGroupModel } from "../models/RequirementGroup"
import { UserModel } from '@/models/User'

const { user } = use_user()

export function generate_config(category_requirement_groups: CategoryRequirementGroupModel[]): Promise<string> {
    return fetch(`${statics.generate_path}`, {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        },
        body: JSON.stringify({ "requirement_groups": category_requirement_groups })
    })
        .then(respo => {
            if (!respo.ok) {
                throw new Error(respo.statusText)
            }
            return respo.json()
        }).then((data: { path: string }) => data.path)
}