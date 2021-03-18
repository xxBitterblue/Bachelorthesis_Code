export type SoftwareModel = {
    software_id: Number,
    name: String,
    version: String,
    type: String,
    dependency_software: SoftwareModel[]
}