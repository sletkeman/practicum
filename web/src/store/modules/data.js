import { GET_DATA } from "../actions";
import { SET_ERROR, SET_DATA, SET_LOADING } from "../mutations";

import { getResults } from "../../services/api";

const state = {
  data: [],
  entropy: 0,
  loading: false,
  edges: [],
  viewers: 0,
  content: 0
};

const actions = {
  async [GET_DATA]({ commit }, [formData]) {
    try {
      commit(SET_LOADING, true);
      const { data } = await getResults(formData);
      const { entropy, results, edges, viewers, content } = data;
      commit(SET_DATA, [results, entropy, edges, viewers, content]);
      commit(SET_LOADING, false);
    } catch (error) {
      commit(SET_ERROR, error);
    }
  }
};

const mutations = {
  [SET_DATA](state, [data, entropy, edges, viewers, content]) {
    state.data = data;
    state.entropy = entropy;
    state.edges = edges;
    state.viewers = viewers;
    state.content = content;
  },
  [SET_LOADING](state, value) {
    state.loading = value;
  }
};

export default {
  state,
  actions,
  mutations
};
