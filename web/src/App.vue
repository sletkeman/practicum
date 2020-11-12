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
        <v-img
          alt="Georgia Tech Logo"
          contain
          :src="require('./assets/gt-logo.svg')"
          width="150"
          @click="togglePage"
        />
      </div>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
    <v-footer :max-height="20" dark color="#b3a369" />
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
    },
    loading(next) {
      if (!next) {
        this.drawer = false;
      }
    }
  },
  methods: {
    togglePage() {
      if (this.$route.name === "Home") {
        this.$router.push("/graph");
      } else {
        this.$router.push("/");
      }
    }
  },
  computed: {
    ...mapState({
      error: state => state.common.error,
      loading: state => state.data.loading
    })
  }
};
</script>
<style scoped>
.sidebar {
  padding: 20px;
}
</style>
