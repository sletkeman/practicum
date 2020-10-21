import Vue from "vue";
import Vuex from "vuex";

import common from "./modules/common";
import data from "./modules/data";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    common,
    data
  }
});
