import { GET_DATA } from "../actions";
import { SET_ERROR, SET_DATA, SET_LOADING } from "../mutations";

import { getResults } from "../../services/api";

const state = {
  data: [],
  entropy: 0,
  loading: false,
  edges: []
};

const actions = {
  async [GET_DATA]({ commit }, [formData]) {
    try {
      commit(SET_LOADING);
      const { data } = await getResults(formData);
      const { entropy, results, edges } = data;
      commit(SET_DATA, [results, entropy, edges]);
      commit(SET_LOADING);
    } catch (error) {
      commit(SET_ERROR, error);
    }
  }
};

const mutations = {
  [SET_DATA](state, [data, entropy, edges]) {
    state.data = data;
    state.entropy = entropy;
    state.edges = edges;
  },
  [SET_LOADING](state) {
    state.loading = !state.loading;
  }
};

export default {
  state,
  actions,
  mutations
};
