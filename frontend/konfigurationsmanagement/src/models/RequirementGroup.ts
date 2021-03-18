import { CategoryModel } from "./Category"
import { SoftwareModel } from "./Software"
import { UserModel } from "./User"

export type RequirementGroupModel = {
    requirement_group_id?: number,
    requirement_group_name: string,
    author?: UserModel,
    status: boolean,
    status_comment: string,
    timestamp?: Date,
    category?: CategoryModel,
    software_list: SoftwareModel[],
    user_comments?: UserCommentsModel[],
    change_history?: ChangeHistoryEntryModel[]
}

export type CategoryRequirementGroupModel = {
    requirement_group_id?: number,
    requirement_group_name: string,
    author?: UserModel,
    status: boolean,
    status_comment: string,
    timestamp?: Date,
    category?: CategoryModel,
    software_list: SoftwareModel[],
    user_comments?: UserCommentsModel[],
    change_history?: ChangeHistoryEntryModel[],
    reference_groups: Number[]
}

export type UserCommentsModel = {
    user_comment_id: number,
    author: UserModel,
    timestamp: Date,
    comment_text: string
}

export type ChangeHistoryEntryModel = {
    change_history_entry_id: number,
    author: UserModel,
    timestamp: Date,
    change_reason?: string,
    changes: JSON
}
