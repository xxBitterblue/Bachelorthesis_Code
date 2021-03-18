import { UserModel } from '@/models/User';

export type DashboardModel = {
    dashboard_entry_id: number,
    type_id: number,
    message: string,
    timestamp: string,
    editor: UserModel
}