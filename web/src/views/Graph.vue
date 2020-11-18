<template>
  <v-container id="graph_container">
    <v-row v-if="loading">
      <div class="centered">
        <v-progress-circular
          indeterminate
          color="primary"
          style="height: 200px;"
          :size="70"
          :width="7"
        ></v-progress-circular>
      </div>
    </v-row>
    <v-row>
      <svg id="graph"></svg>
    </v-row>
  </v-container>
</template>

<script>
import * as d3 from "d3";
import d3Tip from "d3-tip";
import { mapState } from "vuex";

export default {
  name: "Graph",
  data() {
    return {
      recipeId: this.$route.params.id,
      maxNodes: 750,
      colors: [
        "#1b70fc",
        "#faff16",
        "#d50527",
        "#158940",
        "#f898fd",
        "#24c9d7",
        "#cb9b64",
        "#866888",
        "#22e67a",
        "#e509ae",
        "#9dabfa",
        "#437e8a",
        "#b21bff",
        "#ff7b91",
        "#94aa05",
        "#ac5906",
        "#82a68d",
        "#fe6616",
        "#7a7352",
        "#f9bc0f",
        "#b65d66",
        "#07a2e6",
        "#c091ae",
        "#8a91a7",
        "#88fc07",
        "#ea42fe",
        "#9e8010",
        "#10b437",
        "#c281fe",
        "#f92b75",
        "#07c99d",
        "#a946aa",
        "#bfd544",
        "#16977e",
        "#ff6ac8",
        "#a88178",
        "#5776a9",
        "#678007",
        "#fa9316",
        "#85c070",
        "#6aa2a9",
        "#989e5d",
        "#fe9169",
        "#cd714a",
        "#6ed014",
        "#c5639c",
        "#c23271",
        "#698ffc",
        "#678275",
        "#c5a121",
        "#a978ba",
        "#ee534e",
        "#d24506",
        "#59c3fa",
        "#ca7b0a",
        "#6f7385",
        "#9a634a",
        "#48aa6f",
        "#ad9ad0",
        "#d7908c",
        "#6a8a53",
        "#8c46fc",
        "#8f5ab8",
        "#fd1105",
        "#7ea7cf",
        "#d77cd1",
        "#a9804b",
        "#0688b4",
        "#6a9f3e",
        "#ee8fba",
        "#a67389",
        "#9e8cfe",
        "#bd443c",
        "#6d63ff",
        "#d110d5",
        "#798cc3",
        "#df5f83",
        "#b1b853",
        "#bb59d8",
        "#1d960c",
        "#867ba8",
        "#18acc9",
        "#25b3a7",
        "#f3db1d",
        "#938c6d",
        "#936a24",
        "#a964fb",
        "#92e460",
        "#a05787",
        "#9c87a0",
        "#20c773",
        "#8b696d",
        "#78762d",
        "#e154c6",
        "#40835f",
        "#d73656",
        "#1afd5c",
        "#c4f546",
        "#3d88d8",
        "#bd3896",
        "#1397a3",
        "#f940a5",
        "#66aeff",
        "#d097e7",
        "#fe6ef9",
        "#d86507",
        "#8b900a",
        "#d47270",
        "#e8ac48",
        "#cf7c97",
        "#cebb11",
        "#718a90",
        "#e78139",
        "#ff7463",
        "#bea1fd"
      ],
      links: [],
      nodes: {},
      height: 900,
      width: 1700,
      svg: null,
      legend: null,
      simulation: null,
      link: null,
      node: null,
      path: null,
      tip: d3Tip()
        .attr("class", "d3-tip")
        .html(d => {
          if (d.type === "viewer") {
            return `${d.gender} - ${d.age}<br>
            community: ${d.community}<br>
            income: ${d.income}<br>
            education: ${d.education}<br>
            county size: ${d.county_size}`;
          } else {
            return `${d.program_name}<br>
              community: ${d.community}<br>
              network: ${d.network}<br>
              program summary: ${d.program_summary}<br>
              program type: ${d.program_type}li
          `;
          }
        })
    };
  },
  watch: {
    data() {
      if (this.data) {
        this.processData();
        this.render();
      }
    }
  },
  methods: {
    processData() {
      let nodeCount = 0;
      const skipInterval = Math.round(
        (this.content + this.viewers) / this.maxNodes
      );
      this.data.forEach(row => {
        row.children.forEach(child => {
          if (child.name === "Viewers") {
            child.children[0].viewers.forEach(viewer => {
              if (nodeCount % skipInterval === 0) {
                viewer.community = row.name;
                this.nodes[viewer.person_key] = viewer;
              }
              nodeCount += 1;
            });
          } else if (child.name === "Content") {
            child.children[0].content.forEach(item => {
              if (nodeCount % skipInterval === 0) {
                item.community = row.name;
                this.nodes[`${item.content_key}`] = item;
              }
              nodeCount += 1;
            });
          }
        });
      });
      console.log(Object.keys(this.nodes).length);
      this.edges.forEach(e => {
        if (this.nodes[e.PERSONKEY] && this.nodes[`${e.CONTENTSK}`]) {
          this.links.push({
            source: this.nodes[e.PERSONKEY],
            target: this.nodes[`${e.CONTENTSK}`]
          });
        }
      });
    },
    render() {
      this.svg = d3
        .select("svg#graph")
        .attr("width", this.width)
        .attr("height", this.height)
        .attr("style", "border: lightgray 1px solid")
        .call(this.tip);

      // clear the canvas
      this.svg.selectAll("*").remove();

      // start the simulatio
      this.simulation = d3
        .forceSimulation()
        .nodes(d3.values(this.nodes))
        .force("link", d3.forceLink(this.links).distance(50))
        .force("center", d3.forceCenter(this.width / 2, this.height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("charge", d3.forceManyBody().strength(-150))
        .alphaTarget(1)
        .on("tick", this.tick);

      // add the links and the arrows
      this.path = this.svg
        .append("g")
        .selectAll("path")
        .data(this.links)
        .enter()
        .append("path")
        .attr("class", "link");

      // define the nodes
      this.node = this.svg
        .selectAll(".node")
        .data(this.simulation.nodes())
        .enter()
        .append("g")
        .attr("class", "node")
        .on("mouseover", this.tip.show)
        .on("mouseout", this.tip.hide)
        .call(
          d3
            .drag()
            .on("start", this.dragstarted)
            .on("drag", this.dragged)
            .on("end", this.dragended)
        );

      const myColor = d3
        .scaleOrdinal()
        .domain([0, this.data.length])
        .range(this.colors);

      this.node
        .filter(n => n.type === "viewer")
        .append("circle")
        .attr("r", 8)
        .style("fill", d => myColor(d.community));

      this.node
        .filter(n => n.type === "content")
        .append("rect")
        .attr("width", 16)
        .attr("height", 16)
        .style("fill", d => myColor(d.community));

      //   // add a group for the legend
      const legend = this.svg.append("g").attr("id", "legend");
      // outline it with a semi-transparent rectangle
      legend
        .append("rect")
        .attr("fill", "white")
        .attr("stroke", "lightgray")
        .attr("fill-opacity", "0.8")
        .attr("rx", "5px")
        .attr("width", "160px")
        .attr("height", `${this.data.length * 17}px`)
        .attr("x", this.width - 180)
        .attr("y", 10);

      // add the labels
      legend
        .append("text")
        .attr("x", this.width - 85)
        .attr("y", 60)
        .text("Viewer")
        .attr("text-anchor", "left")
        .style("alignment-baseline", "middle");
      legend
        .append("circle")
        .style("fill", "black")
        .attr("cx", this.width - 67)
        .attr("cy", 75)
        .attr("r", 8);
      legend
        .append("text")
        .attr("x", this.width - 85)
        .attr("y", 30)
        .text("Content")
        .attr("text-anchor", "left")
        .style("alignment-baseline", "middle");
      legend
        .append("rect")
        .attr("x", this.width - 75)
        .attr("y", 35)
        .style("fill", "black")
        .attr("width", 16)
        .attr("height", 16);
      legend
        .append("text")
        .attr("x", this.width - 160)
        .attr("y", 30)
        .text("Community")
        .attr("text-anchor", "left")
        .style("alignment-baseline", "middle");
      const communities = this.data.map(d => parseInt(d.name)).sort((a, b) => a - b);
      const labels = legend.selectAll(".labels").data(communities);
      labels
        .enter()
        .append("text")
        .attr("x", this.width - 150)
        .attr("y", (d, i) => 45 + i * 16)
        .text(d => d)
        .attr("text-anchor", "left")
        .style("alignment-baseline", "middle");
      // add the color swatches
      const swatches = legend.selectAll(".swatches").data(communities);
      swatches
        .enter()
        .append("circle")
        .attr("cx", this.width - 130)
        .attr("cy", (d, i) => 45 + i * 16)
        .attr("r", 8)
        .style("fill", d => myColor(d));
    },
    tick() {
      this.path.attr("d", d => {
        const dx = d.target.x - d.source.x;
        const dy = d.target.y - d.source.y;
        const dr = Math.sqrt(dx * dx + dy * dy);
        return (
          "M" +
          d.source.x +
          "," +
          d.source.y +
          "A" +
          dr +
          "," +
          dr +
          " 0 0,1 " +
          d.target.x +
          "," +
          d.target.y
        );
      });

      this.node.attr("transform", d => `translate(${d.x},${d.y})`);
    },
    dragstarted(d) {
      if (!d3.event.active) {
        this.simulation.alphaTarget(0.3).restart();
      }
      d.fx = d.x;
      d.fy = d.y;
    },
    dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    },
    dragended(d) {
      if (!d3.event.active) this.simulation.alphaTarget(0);
      if (d.fixed == true) {
        d.fx = d.x;
        d.fy = d.y;
      } else {
        d.fx = null;
        d.fy = null;
      }
    },
    stopAnimation() {
      this.simulation.stop();
    },
    startAnimation() {
      this.simulation.restart();
    }
  },
  computed: {
    ...mapState({
      data: state => state.data.data,
      entropy: state => state.data.entropy,
      loading: state => state.data.loading,
      edges: state => state.data.edges,
      viewers: state => state.data.viewers,
      content: state => state.data.content
    })
  },
  mounted() {
    if (this.data.length > 0) {
      this.processData();
      this.render();
    }
  }
};
</script>
<style>
.container {
  max-width: 2000px;
}
svg#graph path.link {
  fill: none;
  stroke: lightgray;
}

text {
  fill: #000;
  font: 10px sans-serif;
  pointer-events: none;
}
.centered {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.d3-tip {
  line-height: 1;
  font-weight: bold;
  padding: 12px;
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  border-radius: 2px;
  pointer-events: none;
}

/* Creates a small triangle extender for the tooltip */
.d3-tip:after {
  box-sizing: border-box;
  display: inline;
  font-size: 10px;
  width: 100%;
  line-height: 1;
  color: rgba(0, 0, 0, 0.8);
  position: absolute;
  pointer-events: none;
  content: "\25BC";
  margin: -1px 0 0 0;
  top: 100%;
  left: 0;
  text-align: center;
}
</style>
