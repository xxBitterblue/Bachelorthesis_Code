import { Role } from '../Helper/enums'

export type UserModel = {
    user_id: Number,
    username: String,
    user_role: Role,
    socket_id: String
}