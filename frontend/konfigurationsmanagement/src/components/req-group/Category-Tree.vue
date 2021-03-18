<template>
    <div v-if="category_tree !== undefined">
        <h1 :class="{'caret': !is_expanded, 'caret-down': is_expanded}" @click="expand_tree()">{{category_tree.category_name}}</h1>
        <ul class="tree-root" v-if="is_expanded">
            <li class="tree-child" v-for="category in category_tree.children" :key="category.category_id">
                <Category-Tree-Entry 
                    :entry="category" 
                    @last-category="last_category($event)"
                />
            </li>
        </ul>
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue"
import * as Requirement_Group_APIHelper from "../../Helper/Requirement_Group_APIHelper"
import { CategoryModel, CategoryEntry } from "../../models/Category"
import CategoryTreeEntry from "./Category-Tree-Entry.vue"

    export default defineComponent ({
        name: "Category-Tree",

        components: {
            CategoryTreeEntry
        },

        setup(props, context) {
            let category_list = ref<CategoryModel[]>([])
            let category_tree = ref<CategoryEntry>()
            let is_expanded = ref(false)

             onMounted(async () => {
                category_list.value = await Requirement_Group_APIHelper.get_categorys()
                let root = category_list.value.find(ele => ele.parent.category_id === undefined)
                if(root !== undefined) {
                    category_tree.value = {
                        category_id: root.category_id,
                        category_name: root.category_name,
                        children: []
                    }
                    build_tree_recursive(category_tree.value, category_list.value)
                }
            })

            function expand_tree(){
                is_expanded.value = !is_expanded.value
            }

            function build_tree_recursive(parent:CategoryEntry, categorys: CategoryModel[]){
                for(let category of categorys){
                    if(category.parent.category_id === parent.category_id){
                        let childEntry = {
                            category_id: category.category_id,
                            category_name: category.category_name,
                            children: []
                        }
                        build_tree_recursive(childEntry, categorys)
                        parent.children.push(childEntry)
                    }
                }
            }

            function last_category(category_entry: CategoryEntry) {
                let category = category_list.value.find(category => category.category_id === category_entry.category_id)
                if (category !== undefined) {
                    context.emit("last-category", category)
                }
            }

            return {
                category_list,
                category_tree,
                expand_tree,
                is_expanded,
                last_category
            }
        }
    })
</script>
<style>
.tree-root{
    list-style-type: none;
}
.tree-child{
    margin: 10px;
}
.caret {
  cursor: pointer;
  user-select: none; 
}

.caret::before {
  content: "\25B6";
  color: black;
  display: inline-block;
  margin-right: 6px;
}

.caret-down::before {
  content: "\25B6";
  color: black;
  display: inline-block;
  margin-right: 6px;
  transform: rotate(90deg);
}
</style>