<template>
    <div v-if="category_entry !== undefined">
        <div v-if="category_entry.children.length > 0" @click="is_expanded = !is_expanded">
           <span :class="{'caret': !is_expanded, 'caret-down': is_expanded}">
               {{category_entry.category_name}}
               <button class="btn btn-primary btn-sm" @click.stop="last_category(category_entry)">Auswählen</button>
           </span>
            <ul class="tree-root" v-if="is_expanded">
                <li class="tree-child" v-for="category in category_entry.children" :key="category.category_id">
                    <Category-Tree-Entry
                        :entry="category" 
                        @last-category="last_category($event)"
                    />
                </li>
            </ul>
        </div>
        <div v-else class="tree-child">    
            {{ category_entry.category_name }}
            <button class="btn btn-primary btn-sm" @click.stop="last_category(category_entry)">Auswählen</button>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType, computed, ref } from "vue"
import { CategoryEntry } from "../../models/Category"

    export default defineComponent ({
        name: "Category-Tree-Entry",

        props: {
            entry: {type: Object as PropType<CategoryEntry>, required: true},
        },

        setup(props, context) {
            let category_entry = computed(() => props.entry)
            let is_expanded = ref(false)

            function last_category(category_entry: CategoryEntry) {
                context.emit("last-category", category_entry)
            }

            return {
                is_expanded,
                category_entry,
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