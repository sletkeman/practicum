import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import Graph from "./views/Graph.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home
    },
    {
      path: "/graph",
      name: "Graph",
      component: Graph
    }
  ]
});
