import * as statics from "./statics"
import use_user from "../composable/User"
import { SoftwareModel } from "../models/Software"

const { user } = use_user()

export function get_all(): Promise<SoftwareModel[]> {
    return fetch(`${statics.software_path}`, {
        method: "get",
        headers: { 
            "Content-Type": "application/json", 
            "Authorization": "Token " + user.value["user_token"]
        }
    })
    .then( respo => {
        if(!respo.ok) {
            throw new Error(respo.statusText)
        } 
        return respo.json()
    }).then((data: {software: SoftwareModel[]}) => data.software)
}

export function update_software(software: SoftwareModel): Promise<SoftwareModel> {
    return fetch(`${statics.software_path}update/${software.software_id}/`, {
        method: "post",
        headers: { 
            "Content-Type": "application/json", 
            "Authorization": "Token " + user.value["user_token"]
        },
        body: JSON.stringify(software)
    })
    .then( respo => {
        if(!respo.ok) {
            throw new Error(respo.statusText)
        } 
        return respo.json()
    }).then((data: SoftwareModel) => data)
}

export function add_software(software: SoftwareModel): Promise<SoftwareModel> {
    return fetch(`${statics.software_path}add/`, {
        method: "post",
        headers: { 
            "Content-Type": "application/json", 
            "Authorization": "Token " + user.value["user_token"]
        },
        body: JSON.stringify(software)
    })
    .then( respo => {
        if(!respo.ok) {
            throw new Error(respo.statusText)
        } 
        return respo.json()
    }).then((data: SoftwareModel) => data)
}

export function delete_software(id: Number): Promise<Boolean> {
    return fetch(`${statics.software_path}delete/${id}/`, {
        method: "delete",
        headers: { 
            "Content-Type": "application/json", 
            "Authorization": "Token " + user.value["user_token"]
        }
    })
    .then( respo => {
        if(!respo.ok) {
            //throw new Error(respo.statusText)
            return false
        } 
        return true
    })
}