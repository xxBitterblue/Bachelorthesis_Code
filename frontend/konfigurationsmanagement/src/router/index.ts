import { createRouter, createWebHistory } from 'vue-router'
import Authentification from '../components/auth/Authentification.vue'
import Group_Overview from '../components/req-group/Group-Overview.vue'
import Software_Overview from '../components/software/Software-Overview.vue'
import Add_Req_Group from '../components/req-group/Add-Req-Group.vue'
import Add_Cat_Req_Group from '../components/req-group/Add-Cat-Req-Group.vue'
import Group_Detail_Page from '../components/req-group/Group-Detail-Page.vue'
import Validation_Overview from '../components/validation/Validation-Overview.vue'
import Update_Validation_Rule from '../components/validation/Update-Validation-Rule-View.vue'
import Generate_Config from "../components/req-group/Generate-Config.vue"
import Dashboard from "../components/Dashboard.vue"

const routes = [
  {
    path: '/',
    name: 'Authentification',
    component: Authentification
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/req_group_overview',
    name: 'Group_Overview',
    component: Group_Overview
  },
  {
    path: '/group_details_overview/:id',
    name: 'Group_Detail_Page',
    component: Group_Detail_Page,
    props: true
  },
  {
    path: '/add_req_group',
    name: 'Add_Req_Group',
    component: Add_Req_Group
  },
  {
    path: '/add_req_group/:id',
    name: 'Edit_Req_Group',
    component: Add_Req_Group,
    props: true
  },
  {
    path: '/add_cat_req_group',
    name: 'Add_Cat_Req_Group',
    component: Add_Cat_Req_Group
  },
  {
    path: '/add_cat_req_group/:id',
    name: 'Edit_Cat_Req_Group',
    component: Add_Cat_Req_Group,
    props: true
  },
  {
    path: '/software_overview',
    name: 'Software_Overview',
    component: Software_Overview
  },
  {
    path: '/validation',
    name: 'Validation_Overview',
    component: Validation_Overview
  },
  {
    path: '/update_validation_rule',
    name: 'Add_Validation_Rule',
    component: Update_Validation_Rule
  },
  {
    path: '/update_validation_rule/:id',
    name: 'Update_Validation_Rule',
    component: Update_Validation_Rule,
    props: true
  },
  {
    path: '/generate_config',
    name: 'Generate_Config',
    component: Generate_Config
  }
]

const routerHistory = createWebHistory()

const router = createRouter({
  history: routerHistory,
  routes
})

export default router