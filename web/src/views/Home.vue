<template>
  <v-treeview :items="data">
    <template v-slot:label="{ item }">
      <div v-if="Object.keys(item).includes('content')">
        <v-data-table
          :headers="contentHeaders"
          :items="item.content"
          :disable-pagination="true"
        ></v-data-table>
      </div>
      <div v-else-if="Object.keys(item).includes('viewers')">
        <v-data-table
          :headers="viewerHeaders"
          :items="item.viewers"
          :disable-pagination="true"
        ></v-data-table>
      </div>
      <div v-else>
        {{ item.name }} - {{ item.id }} ({{ item.children.length }} items)
      </div>
    </template>
  </v-treeview>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "Practicum",
  data() {
    return {
      viewerHeaders: [
        { text: "Age", value: "age" },
        { text: "Gender", value: "gender" },
        { text: "income", value: "income" },
        { text: "County Size", value: "county_size" },
        { text: "Education", value: "education" }
      ],
      contentHeaders: [
        { text: "Program Name", value: "program_name" },
        { text: "Program Summary", value: "program_summary" },
        { text: "Program Type", value: "program_type" }
      ]
    };
  },
  methods: {
    ...mapActions([])
  },
  computed: {
    ...mapState({
      data: state => state.data.data
    })
  },
  async mounted() {}
};
</script>
