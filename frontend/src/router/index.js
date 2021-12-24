import VueRouter from 'vue-router'
import user from './user'
import account from './account'
import manage from './manage'
import system from './system'
import basicData from './basicData'
import goods from './goods'
import purchasing from './purchasing'

const index = {
  path: '/',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/home',
  children: [
    {
      path: '/home',
      name: 'home',
      meta: { title: '首页' },
      component: () => import('@/views/home/Home'),
    },
  ]
}

const routes = [index, user, account, manage, system, basicData, goods, purchasing];

export default new VueRouter({ mode: 'history', routes })
