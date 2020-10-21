import { GET_DATA } from "../actions";
import { SET_ERROR, SET_DATA } from "../mutations";

import { getResults } from "../../services/api";

const state = {
  data: []
};

const actions = {
  async [GET_DATA]({ commit }, [formData]) {
    try {
      const { data } = await getResults(formData);
      commit(SET_DATA, data);
    } catch (error) {
      commit(SET_ERROR, error);
    }
  }
};

const mutations = {
  [SET_DATA](state, data) {
    state.data = data;
  }
};

export default {
  state,
  actions,
  mutations
};
