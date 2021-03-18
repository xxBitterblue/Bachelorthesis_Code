import { CategoryModel } from "./Category"
import { UserModel } from "./User"
import { SoftwareModel } from '@/models/Software';

export type ValidationRuleModel = {
    validation_rule_id: Number,
    name: String,
    author?: UserModel,
    active: Boolean,
    is_global: Boolean,
    rule: String,
    categorys: CategoryModel[]
}

export type ValidationStructureModel = {
    software_structure: {
        software_list: SoftwareModel[]

    },
    exception_options: string[]
}