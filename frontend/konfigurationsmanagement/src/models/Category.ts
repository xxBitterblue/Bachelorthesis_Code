export type CategoryModel = {
    category_id: Number,
    category_name: String,
    parent: CategoryModel
    children: CategoryModel[]
}

export type CategoryEntry = {
    category_id: Number,
    category_name: String,
    children: CategoryEntry[]
}