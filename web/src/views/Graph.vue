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
      colors: [
        "maroon",
        "red",
        "purple",
        "fuchsia",
        "green",
        "lime",
        "olive",
        "yellow",
        "navy",
        "blue",
        "teal",
        "aqua",
        "orange",
        "blueviolet",
        "brown",
        "burlywood",
        "cadetblue",
        "chartreuse",
        "chocolate",
        "coral",
        "cornflowerblue",
        "cornsilk",
        "crimson",
        "darkblue",
        "darkcyan"
      ],
      links: [],
      nodes: {},
      height: 1500,
      width: 1500,
      svg: null,
      legend: null,
      simulation: null,
      link: null,
      node: null,
      path: null,
      tip: d3Tip()
        .attr("class", "d3-tip")
        .html(d => {
          if (d.type === 'viewer') {
            return `gender: ${d.gender || 'N/A'}`;
          } else {
            return d.program_name;
          }
        })
        // .html(function(d) {
        //   if (d.type === "viewer") {
        //     return `personKey: ${d.person_key}<br>`;
        //     // age: ${v.age}<br>
        //     // income: ${v.income}<br>
        //     // gender: ${v.gender}<br>
        //     // education: ${v.education}<br>
        //     // county size: ${v.county_size}`;
        //   } else {
        //     return `contentKey: ${d.content_key}<br>`;
        //     //     network": ${c.network}<br>
        //     //     program name: ${c.program_name}<br>
        //     //     program summary: ${c.program_summary}<br>
        //     //     program type: ${c.program_type}<br>
        //     // `;
        //   }
        // })
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
      //   let viewerCount = 0;
      this.data.forEach(row => {
        row.children.forEach(child => {
          if (child.name === "Viewers") {
            child.children[0].viewers.forEach(viewer => {
              //   if (viewerCount % 2 === 0) {
              viewer.community = row.name;
              this.nodes[viewer.person_key] = viewer;
              //   }
              //   viewerCount += 1;
            });
          } else if (child.name === "Content") {
            child.children[0].content.forEach(item => {
              item.community = row.name;
              this.nodes[`${item.content_key}`] = item;
            });
          }
        });
      });
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
        .force("link", d3.forceLink(this.links).distance(5))
        .force("center", d3.forceCenter(this.width / 2, this.height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("charge", d3.forceManyBody().strength(-50))
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

      // add the nodes
      //   let maxWeight = 0;
      this.node
        .filter(n => n.type === "viewer")
        .append("circle")
        .attr("r", 3)
        .style("fill", d => this.colors[d.community]);
      // .attr("r", d => {
      //   d.weight = this.links.filter(
      //     l => l.source.index == d.index || l.target.index == d.index
      //   ).length;
      //   if (d.weight > maxWeight) {
      //     maxWeight = d.weight;
      //   }
      //   return 10;
      // });

      // make recipe nodes a Wye symbol
      this.node
        .filter(n => n.type === "content")
        .append("rect")
        .attr("width", 6)
        .attr("height", 6)
        .style("fill", d => this.colors[d.community]);
      // .append("path")
      // .attr("d", d =>
      //   d3
      //     .symbol()
      //     .type(d3.symbolWye)
      //     .size(1000 * d.score)()
      // );

      // set up the yellow-green color gradient for the ingredients
      //   const gradient = d3
      //     .scaleLinear()
      //     .domain([1, maxWeight])
      //     .range(["yellow", "darkgreen"]);

      // add the recipe and ingredient names
      //   this.node
      //     .append("text")
      //     .text(d => d.name)
      //     .attr("transform", "translate(0,10)")
      //     .style("font-weight", "bold")

      // add color to the nodes
      //   this.node.style("fill", d =>
      //     d.type === "ingredient" ? gradient(d.weight) : "mediumorchid"
      //   );

      //   // add a group for the legend
      //   const legend = this.svg.append("g").attr("id", "legend");
      //   // outline it with a semi-transparent rectangle
      //   legend
      //     .append("rect")
      //     .attr("fill", "white")
      //     .attr("stroke", "lightgray")
      //     .attr("fill-opacity", "0.8")
      //     .attr("rx", "5px")
      //     .attr("width", "90px")
      //     .attr("height", "205px")
      //     .attr("x", this.width - 180)
      //     .attr("y", 10);

      //   // add the labels
      //   legend
      //     .append("text")
      //     .attr("x", this.width - 155)
      //     .attr("y", 30)
      //     .text("Recipes")
      //     .attr("text-anchor", "left")
      //     .style("alignment-baseline", "middle");
      //   legend
      //     .append("path")
      //     .style("fill", "mediumorchid")
      //     .attr("transform", `translate(${this.width - 135}, ${60})`)
      //     .attr(
      //       "d",
      //       d3
      //         .symbol()
      //         .type(d3.symbolWye)
      //         .size(500)()
      //     );
      //   legend
      //     .append("text")
      //     .attr("x", this.width - 160)
      //     .attr("y", 100)
      //     .text("Ingredients")
      //     .attr("text-anchor", "left")
      //     .style("alignment-baseline", "middle");
      //   legend
      //     .append("text")
      //     .attr("x", this.width - 160)
      //     .attr("y", 115)
      //     .text("in-degree")
      //     .attr("text-anchor", "left")
      //     .style("alignment-baseline", "middle");

      //   // prepare to demonstrate the gradient
      //   const vals = [1, Math.round(maxWeight / 2), maxWeight];
      //   const labels = legend.selectAll(".labels").data(vals);
      //   labels
      //     .enter()
      //     .append("text")
      //     .attr("x", this.width - 130)
      //     .attr("y", (d, i) => 140 + i * 30)
      //     .text(d => d)
      //     .attr("text-anchor", "left")
      //     .style("alignment-baseline", "middle");
      //   // add the color swatches
      //   const swatches = legend.selectAll(".swatches").data(vals);
      //   swatches
      //     .enter()
      //     .append("circle")
      //     .attr("cx", this.width - 150)
      //     .attr("cy", (d, i) => 138 + i * 30)
      //     .attr("r", 10)
      //     .style("fill", d => gradient(d));
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
      edges: state => state.data.edges
    })
  },
  mounted() {
    if (this.data) {
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
