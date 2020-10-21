<template>
  <v-treeview :items="data">
    <template v-slot:label="{ item }">
      <div v-if="Array.isArray(item)">
          <div>
            Viewer: {{item.filter(i => i.type === 'viewer').length}}
              <!-- <v-data-table
                :headers="viewerHeaders"
                :items="item.data.filter(i => i.type === 'viewer')"
                :disable-pagination="true"
              ></v-data-table> -->
          </div>
          <div>
            Content: {{item.filter(i => i.type === 'content').length}}
              <!-- <v-data-table
                :headers="contentHeaders"
                :items="item.data.filter(i => i.type === 'content')"
                :disable-pagination="true"
              ></v-data-table> -->
          </div>
      </div>
      <div v-else>
        {{ item.name }} ({{ item.children.length }} items)
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
        { text: "County Size", value: "county_size" },
        { text: "Education", value: "education" },
        { text: "Gender", value: "gender" },
        { text: "income", value: "Income" }
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
