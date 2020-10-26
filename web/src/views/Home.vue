<template>
<div>
  <v-card>
    <v-card-title>
    Entropy
    </v-card-title>
    <v-card-text>
     {{entropy | round}}
    </v-card-text>
  </v-card>
  <v-treeview :items="data" dense>
    <template v-slot:label="{ item }">
      <div v-if="Object.keys(item).includes('content')">
        <v-data-table
          :headers="contentHeaders"
          :items="item.content"
          :disable-pagination="true"
          :dense="true"
          :hide-default-footer="true"
        ></v-data-table>
      </div>
      <div v-else-if="Object.keys(item).includes('viewers')">
        <v-data-table
          :headers="viewerHeaders"
          :items="item.viewers"
          :disable-pagination="true"
          :dense="true"
          :hide-default-footer="true"
        ></v-data-table>
      </div>
      <div v-else-if="item.children[0].content">
        {{ item.name }} ({{ item.children[0].content.length }})
      </div>
      <div v-else-if="item.children[0].viewers">
        {{ item.name }} ({{ item.children[0].viewers.length }})
      </div>
      <div v-else>{{ item.name }} (viewers: {{ item.viewer_count }}, content: {{item.content_count}})</div>
    </template>
  </v-treeview>
</div>
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
        { text: "Program Type", value: "program_type" },
        { text: "Primary Network", value: "network"}
      ]
    };
  },
  filters: {
    round(val) {
      return Math.round(val).toLocaleString()
    }
  },
  methods: {
    ...mapActions([])
  },
  computed: {
    ...mapState({
      data: state => state.data.data,
      entropy: state => state.data.entropy
    })
  },
  async mounted() {}
};
</script>
