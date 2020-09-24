<template>
  <div class="allergen">
    Allergen
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "Allergen",
  data() {
    return {
      headers: [
        { text: "Allergen Type", value: "group" },
        { text: "Number of Ingredients", value: "ingredients" }
      ]
    };
  },
  methods: {
    ...mapActions(["GET_ALLERGENS"])
  },
  computed: {
    ...mapState({
      // allergens: state => state.recipe.allergens
    })
  },
  async mounted() {
    // await this.GET_ALLERGENS();
  }
};
</script>
