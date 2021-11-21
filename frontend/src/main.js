import VueRouter from 'vue-router'
import router from './router'
import App from './App.vue'
import Vue from 'vue'


Vue.config.productionTip = false;
Vue.use(VueRouter);
if (process.env.NODE_ENV == 'development') {
  Vue.config.devtools = true;
} else {
  Vue.config.devtools = false;
}
new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
