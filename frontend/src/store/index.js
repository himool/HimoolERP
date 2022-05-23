import Vuex from 'vuex'
import user from './modules/user'
import system from './modules/system'
import Vue from 'vue'

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user,
    system,
  },
})