import Vuex from 'vuex'
import user from './modules/user'
import system from './modules/system'

export default new Vuex.Store({
  modules: {
    user,
    system,
  },
})