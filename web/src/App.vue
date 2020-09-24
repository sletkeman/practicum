<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      app
      clipped
      right
      :width="350"
      class="sidebar"
    >
      <SearchForm />
    </v-navigation-drawer>
    <v-app-bar app dark style="background-color:#b3a369" clipped-right>
      <div class="d-flex align-center">
        <router-link :to="{ name: 'Home' }">
          <v-img
            alt="Georgia Tech Logo"
            contain
            :src="require('./assets/gt-logo.svg')"
            width="150"
          />
        </router-link>
      </div>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import { mapState } from "vuex";
import SearchForm from "./components/searchForm";

export default {
  components: { SearchForm },
  data() {
    return {
      drawer: null
    };
  },
  watch: {
    error(message) {
      this.$notify.error({
        title: "Error",
        message,
        position: "bottom-left"
      });
    }
  },
  methods: {
    goHome() {
      this.$router.push("/");
    }
  },
  computed: {
    ...mapState({
      error: state => state.common.error
    })
  }
};
</script>
<style scoped>
.sidebar {
  padding: 20px;
}
</style>
