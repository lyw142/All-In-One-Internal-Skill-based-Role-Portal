import "bootstrap/dist/css/bootstrap.css"
import "bootstrap/dist/js/bootstrap.js"
import { createApp } from 'vue'
import {createRouter, createWebHistory} from 'vue-router'
import App from './App.vue'

// routes
import Home from './views/Home.vue'
import StaffNavigation from './components/StaffNavigation.vue'
import HRNavigation from './components/HRNavigation.vue'
import UpdateRoleListing from './views/UpdateRoleListing.vue'
import CreateRoleListing from './views/CreateRoleListing.vue'
import ApplicationHistory from './views/ApplicationHistory.vue'
import Candidates from './components/Candidates.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', name:'Home', component: Home},
        {path: '/staffnav', name:'StaffNav', component: StaffNavigation},
        {path: '/hrnav', name:'HRNav', component: HRNavigation},
        {path: '/updaterolelisting/:Listing_ID', name:'UpdateRoleListing', component: UpdateRoleListing, props: true},
        {path: '/createrolelisting', name:'CreateRoleListing', component: CreateRoleListing},
        {path: '/application-history', name:'ApplicationHistory', component: ApplicationHistory},
        {path: '/candidates', name: 'Candidates', component: Candidates},
    ]
})

createApp(App).use(router).mount('#app')

