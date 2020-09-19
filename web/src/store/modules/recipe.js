import { GET_ALLERGENS } from "../actions";
import { SET_ERROR, SET_ALLERGENS } from "../mutations";

import { fetchAllergens } from "../../services/api";

const state = {
  allergens: []
};

const actions = {
  async [GET_ALLERGENS]({ commit, state }) {
    if (state.allergens.length === 0) {
      try {
        const { data } = await fetchAllergens();
        commit(SET_ALLERGENS, data);
      } catch (error) {
        commit(SET_ERROR, error);
      }
    }
  }
};

const mutations = {
  [SET_ALLERGENS](state, allergens) {
    state.allergens = allergens;
  }
};

export default {
  state,
  actions,
  mutations
};
