import VueRouter from 'vue-router'
import router from './router'
import App from './App.vue'
import Vue from 'vue'
// import './mock'

Vue.config.productionTip = false;
Vue.use(VueRouter);

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
