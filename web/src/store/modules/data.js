import { GET_DATA } from "../actions";
import { SET_ERROR, SET_DATA } from "../mutations";

import { getResults } from "../../services/api";

const state = {
  data: [],
  entropy: 0
};

const actions = {
  async [GET_DATA]({ commit }, [formData]) {
    try {
      const { data } = await getResults(formData);
      const { entropy, results } = data;
      commit(SET_DATA, [results, entropy] );
    } catch (error) {
      commit(SET_ERROR, error);
    }
  }
};

const mutations = {
  [SET_DATA](state, [data, entropy]) {
    state.data = data;
    state.entropy = entropy;
  }
};

export default {
  state,
  actions,
  mutations
};
