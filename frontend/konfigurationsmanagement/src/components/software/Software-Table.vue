<template>
    <div class="row">
        <div class="col-4 mb-8">
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">Filter:</span>
                </div>
                <input type="text" class="form-control" v-model="filter">
            </div>
        </div>
    </div>
    <div class="scrollable">
        <table class="table table-sm table-striped table-hover"
            @dragover.prevent
            @drop.prevent="drop"
            :key="software_list"
        >
            <thead>
                <tr>
                    <th scope="col"></th>
                    <th scope="col">
                        Name
                        <button class="btn btn-outline-secondary btn-sm" v-on:click="sort_table('name', 'desc')">v</button>
                        <button class="btn btn-outline-secondary btn-sm" v-on:click="sort_table('name', 'asc')">^</button>
                    </th>
                    <th scope="col">
                        Version
                        <button class="btn btn-outline-secondary btn-sm" v-on:click="sort_table('version', 'desc')">v</button>
                        <button class="btn btn-outline-secondary btn-sm" v-on:click="sort_table('version', 'asc')">^</button>
                    </th>
                    <th scope="col">
                        Type
                        <button class="btn btn-outline-secondary btn-sm" v-on:click="sort_table('type', 'desc')">v</button>
                        <button class="btn btn-outline-secondary btn-sm" v-on:click="sort_table('type', 'asc')">^</button>
                    </th>
                    <th v-if="editAllowed" scope="col"></th>
                    <th v-if="editAllowed" scope="col"></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="software in software_list" :key="software.software_id"
                    :draggable='dragAllowed'
                    @dragstart="dragStart($event, software)"
                    @dragend="dragEnd($event, software)">
                    <td>
                        <button class="btn btn-outline-secondary" v-if="current_extended_software_row == -1 || current_extended_software_row != software.software_id" v-on:click="show_dependency_software(software)">
                            Zeige Abhängigkeiten
                        </button>
                        <button class="btn btn-outline-secondary" v-if="current_extended_software_row != -1 && current_extended_software_row == software.software_id" v-on:click="close_dependency_software()">
                            Schließe Abhängigkeiten
                        </button>
                    </td>
                    <td>{{ software.name }}</td>
                    <td>{{ software.version }}</td>
                    <td>{{ software.type }}</td>
                    <td v-if="editAllowed">
                        <button class="btn btn-outline-secondary" v-on:click="delete_software(software.software_id)">
                            Löschen
                        </button>
                    </td>
                    <td v-if="editAllowed">
                        <button class="btn btn-outline-secondary" v-on:click="update_software(software)">
                            Bearbeiten
                        </button>
                    </td>
                    <div v-if="current_extended_software_row == software.software_id">
                        <Software-Table
                            v-if="software.dependency_software.length > 0"
                            :softwareList="software.dependency_software"
                            :editAllowed="false"
                        />  
                        <p v-else>Keine Abhängigkeiten</p>     
                    </div>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType, computed, ref, onMounted } from "vue"
import { SoftwareModel } from "../../models/Software"

 export default defineComponent ({
    name: "Software-Table",
    
    emits: ["delete-software", "update-software", "software-changed"],

    props: {
        softwareList: {type: Object as PropType<SoftwareModel[]>, required: true},
        changeInfoActive: {type: Boolean, required: false},
        editAllowed: {type: Boolean},
        dragAllowed: {type: Boolean},
        requirementGroupId: {type: Number, required:false}
    },

    setup(props, context) {
        let filter = ref('')
        let sort = ref({direction: '', row: ''})
        let software_list = computed(() => {
            let current_list = props.softwareList
            if(filter.value !== ''){
                current_list = current_list.filter(
                    ele => ele.name.toLowerCase().includes(filter.value) 
                    || ele.version.toLowerCase().includes(filter.value)
                    || ele.type.toLowerCase().includes(filter.value)
                )
            }
            if(sort.value.row !== ''){
                if(sort.value.direction === 'asc'){
                    current_list = current_list.sort((a,b) => a[sort.value.row] > b[sort.value.row] ? -1 : 1)
                }else if(sort.value.direction === 'desc'){
                    current_list = current_list.sort((a,b) => a[sort.value.row] > b[sort.value.row] ? 1 : -1)
                }
            }
          return current_list
        })
        let current_extended_software_row = ref(-1)
        
        function delete_software(id: Number) {
            context.emit("delete-software", id)
        }

        function update_software(software) {
            context.emit("update-software", software)
        }

        function show_dependency_software(software) {
            current_extended_software_row.value = software.software_id
        }

        function close_dependency_software() {
            current_extended_software_row.value = -1
        }

        function sort_table(row, direction){
            if(row === sort.value.row){
                if(sort.value.direction !== direction){
                    sort.value = {direction, row}
                }else {
                    sort.value = {direction: '', row: ''}
                }
            }else{
                sort.value = {direction, row}
            }
        }

        function dragStart(e, software) {
            e.dataTransfer.dropEffect = "copy"
            e.dataTransfer.setData('software', JSON.stringify(software))
            if(props.requirementGroupId !== undefined){
                e.dataTransfer.setData('req_group_id', props.requirementGroupId)
            }
        }

        function dragEnd(e, software){
            if(!(e.dataTransfer.dropEffect === 'none' && e.dataTransfer.effectAllowed === 'uninitialized')){
                filter.value = ''
                let software_idx = software_list.value.indexOf(software)
                software_list.value.splice(software_idx, 1)
            }
        }

        function drop(e) {
            filter.value = ''
            const software = JSON.parse(e.dataTransfer.getData('software'))
            const id = e.dataTransfer.getData('req_group_id')
            software_list.value.push(software)
            if (props.changeInfoActive) {
                if (id !== undefined) {
                    context.emit("software-changed", id)
                } else {
                    context.emit("software-changed")
                }
            }
        }

        return {
            software_list,
            sort,
            filter,
            sort_table,
            dragStart,
            dragEnd,
            drop,
            delete_software,
            update_software,
            show_dependency_software,
            close_dependency_software,
            current_extended_software_row
        }
    },
 })
</script>
<style>
.scrollable{
    height: 342px !important;
    overflow: scroll;
}
</style>