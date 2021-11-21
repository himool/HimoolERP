import VueRouter from 'vue-router'
import invoice from './invoice'
import console from './console'
import user from './user'

const routes = [console, user, invoice];

export default new VueRouter({ mode: 'history', routes })
