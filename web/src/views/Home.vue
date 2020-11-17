<template>
  <div style="height:100%">
    <v-row
      class="contentRow"
      v-if="viewerActive && activeItem.viewer_count > 0"
    >
      <v-col :cols="3" class="contentCol">
        <div>
          <v-row>
            <v-col>
              <h4>
                Viewer
              </h4>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              Average Age:
              {{
                (activeItem.viewer_aggs.age / activeItem.viewer_count) | round
              }}
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              Average Income:
              ${{
                (activeItem.viewer_aggs.income / activeItem.viewer_count)
                  | round
              }},000
            </v-col>
          </v-row>
        </div>
      </v-col>
      <v-col :cols="3" class="contentCol">
        <h4>Gender</h4>
        <apexchart
          :options="{
            ...viewerOptions,
            xaxis: {
              categories: Object.keys(activeItem.viewer_aggs.gender)
            }
          }"
          :series="[{ data: Object.values(activeItem.viewer_aggs.gender) }]"
        ></apexchart>
      </v-col>
      <v-col :cols="3" class="contentCol">
        <h4>
          Education
        </h4>
        <apexchart
          :options="{
            ...viewerOptions,
            xaxis: {
              categories: Object.keys(activeItem.viewer_aggs.education)
            }
          }"
          :series="[{ data: Object.values(activeItem.viewer_aggs.education) }]"
        ></apexchart>
      </v-col>
      <v-col :cols="3" class="contentCol">
        <h4>
          County Size
        </h4>
        <apexchart
          :options="{
            ...viewerOptions,
            xaxis: {
              categories: Object.keys(activeItem.viewer_aggs.county_size)
            }
          }"
          :series="[
            { data: Object.values(activeItem.viewer_aggs.county_size) }
          ]"
        ></apexchart>
      </v-col>
    </v-row>
    <v-row
      class="contentRow"
      v-else-if="!viewerActive && activeItem.content_count > 0"
    >
      <v-col :cols="4" class="contentCol">
        <h4>Program Summary</h4>
        <apexchart
          :options="{
            ...contentOptions,
            xaxis: {
              categories: Object.keys(activeItem.content_aggs.program_summary)
            }
          }"
          :series="[
            { data: Object.values(activeItem.content_aggs.program_summary) }
          ]"
        ></apexchart>
      </v-col>
      <v-col :cols="4" class="contentCol">
        <h4>
          Program Type
        </h4>
        <apexchart
          :options="{
            ...contentOptions,
            xaxis: {
              categories: Object.keys(activeItem.content_aggs.program_type)
            }
          }"
          :series="[
            { data: Object.values(activeItem.content_aggs.program_type) }
          ]"
        ></apexchart>
      </v-col>
      <v-col :cols="4" class="contentCol">
        <h4>
          Primary Network
        </h4>
        <apexchart
          :options="{
            ...contentOptions,
            xaxis: {
              categories: Object.keys(activeItem.content_aggs.network)
            }
          }"
          :series="[{ data: Object.values(activeItem.content_aggs.network) }]"
        ></apexchart>
      </v-col>
    </v-row>
    <v-row v-else class="contentRow"></v-row>
    <hr />
    <div v-if="loading" style="width:100%;text-align:center;padding-top:100px">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>
    <div v-else>
    Entropy: {{ entropy | round }}
    <v-treeview :items="data" dense :style="`height:${tableHeight}px`" >
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
          {{ item.name }} - {{ item.children[0].content.length }}
        </div>
        <div v-else-if="item.children[0].viewers">
          {{ item.name }} - {{ item.children[0].viewers.length }}
        </div>
        <div v-else>
          {{ item.name }} -
          <span @mouseenter="handleMouseEnter(item, 'viewer')"
            >viewers: {{ item.viewer_count }},
          </span>
          <span @mouseenter="handleMouseEnter(item, 'content')"
            >content: {{ item.content_count }}</span
          >
        </div>
      </template>
    </v-treeview>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

// import VueApexCharts from 'vue-apexcharts'

export default {
  name: "Practicum",
  data() {
    return {
      windowHeight: window.innerHeight,
      sidebarOpen: true,
      mini: false,
      viewerActive: true,
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
        { text: "Primary Network", value: "network" }
      ],
      activeItem: {},
      viewerOptions: {
        chart: {
          type: "bar",
          height: 250
        },
        plotOptions: {
          bar: { horizontal: true }
        },
        dataLabels: { enabled: false }
      },
      contentOptions: {
        chart: {
          type: "bar"
        },
        plotOptions: {
          bar: { horizontal: true }
        },
        dataLabels: { enabled: false }
      },
      county_size: {
        "“A” county -25 largest metropolitan areas": 11,
        "“B” county -over 150,000 in population, but not an “A” county": 10,
        "“C” county -over 40,000 in population, but not an “A” or “B” county": 5,
        "“D” county -all others": 3
      }
    };
  },
  filters: {
    round(val) {
      return Math.round(val).toLocaleString();
    }
  },
  methods: {
    ...mapActions([]),
    handleMouseEnter(item, type) {
      this.activeItem = item;
      this.viewerActive = type === "viewer";
    },
    handleMouseLeave() {
      // this.activeItem = {};
    },
    addSizeChangeListener() {
      const self = this;
      window.addEventListener("resize", () => {
        self.windowHeight = window.innerHeight;
      });
    }
  },
  computed: {
    ...mapState({
      data: state => state.data.data,
      entropy: state => state.data.entropy,
      loading: state => state.data.loading
    }),
    tableHeight() {
      return this.windowHeight - 380;
    }
  },
  async mounted() {
    this.addSizeChangeListener();
  }
};
</script>
<style scoped>
.v-treeview {
  overflow-y: scroll;
}
.contentRow {
  height: 300px;
  min-height: 300px;
  max-height: 300px;
  padding-right: 10px;
}
.contentCol {
  height: 300px;
  overflow-y: scroll;
  padding-left: 30px;
  padding-right: 10px;
}
</style>
