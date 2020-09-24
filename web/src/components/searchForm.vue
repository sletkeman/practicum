<template>
  <div>
    <v-form ref="form" v-model="valid">
      <v-list expand>
        <v-list-group :value="expanded.model">
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title>Model</v-list-item-title>
            </v-list-item-content>
          </template>
          <v-switch
            label="Use Nested Model"
            v-model="form.useNestedModel"
            class="ma-4"
          ></v-switch>
          <v-switch
            label="Use Degree Correction"
            v-model="form.useDegreeCorrection"
            class="ma-4"
          ></v-switch>
          <v-switch
            label="Use Edge Weights"
            v-model="form.useEdgeWeights"
            class="ma-4"
          ></v-switch>
          <v-text-field
            label="Sample Size"
            v-model="form.sampleSize"
            class="ma-4"
            type="number"
          ></v-text-field>
        </v-list-group>
        <v-list-group :value="expanded.content">
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title>Content</v-list-item-title>
            </v-list-item-content>
          </template>
          <v-text-field
            label="Program Name"
            v-model="form.programName"
            class="ma-4"
          ></v-text-field>
          <v-select
            label="Program Category"
            v-model="form.programCategory"
            class="ma-4"
            :items="programCategories"
            :clearable="true"
          ></v-select>
          <v-autocomplete
            label="Program Type Summary"
            v-model="form.programTypeSummary"
            class="ma-4"
            :items="filteredTypeSummary"
            :clearable="true"
            :search-input.sync="typeSummaryFilterText"
          ></v-autocomplete>
          <v-autocomplete
            label="Program Type"
            v-model="form.programType"
            class="ma-4"
            :items="filteredProgramType"
            :clearable="true"
            :search-input.sync="programTypeFilterText"
          ></v-autocomplete>
          <v-autocomplete
            label="Network"
            v-model="form.network"
            class="ma-4"
            :items="filteredNetwork"
            :clearable="true"
            :search-input.sync="networkFilterText"
          ></v-autocomplete>
        </v-list-group>
      </v-list>
    </v-form>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "SearchForm",
  data() {
    return {
      valid: true,
      expanded: {
        model: false,
        content: true
      },
      form: {
        useNestedModel: true,
        useDegreeCorrection: true,
        useEdgeWeights: false,
        sampleSize: 250,
        programName: "",
        programCategory: "",
        programTypeSummary: "",
        programType: "",
        network: ""
      },
      programCategories: ["SERIES", "FEATURE FILM"],
      filteredTypeSummary: [],
      typeSummaryFilterText: "",
      programTypeSummary: [
        "PARTICIPATION VARIETY",
        "EVENING ANIMATION",
        "SPORTS ANTHOLOGY",
        "GENERAL DRAMA",
        "SCIENCE FICTION",
        "POPULAR MUSIC",
        "NEWS DOCUMENTARY",
        "ADVENTURE",
        "GENERAL VARIETY",
        "SITUATION COMEDY",
        "CHILD MULTI-WEEKLY",
        "GENERAL DOCUMENTARY",
        "WESTERN DRAMA",
        "SUSPENSE/MYSTERY",
        "INSTRUCTION, ADVICE",
        "FEATURE FILM",
        "PARTICIPATION VARIETY"
      ],
      filteredProgramType: [],
      programTypeFilterText: "",
      nhiProgramType: [
        "NHIPROGRAMTYPE",
        "DOCUMENTARY - OTHER",
        "SERIES - DRAMA",
        "DOCUMENTARY - CURRENT EVENTS",
        "UNCLASSIFIED",
        "CHILDREN - SERIES/ANIMATED",
        "INSTRUCT/INFO - PARENTING",
        "NEWS - DOCUMENTARY",
        "MUSIC VIDEOS - SERIES",
        "MUSIC - OTHER",
        "DOCUMENTARY - ADVENTURE",
        "SERIES - FAMILY",
        "DOCUMENTARY - NATURE",
        "INSTRUCT/INFO - HOME IMPROVEME",
        "CHILDREN - SERIES/OTHER",
        "COLLEGE FOOTBALL-ANTHOLOGY",
        "SERIES - SCIENCE FICTION",
        "DOCUMENTARY - PERSONALITIES",
        "NOVELA",
        "DOCUMENTARY - HISTORY",
        "COMEDY - VARIETY",
        "DOCUMENTARY - SPECIAL",
        "COMEDY - SKITS",
        "OTHER SPORTS-ANTHOLOGY",
        "PRO FOOTBALL-ANTHOLOGY",
        "DOCUMENTARY - WEATHER",
        "DOCUMENTARY - MOVIES",
        "PRO BASKETBALL-ANTHOLOGY",
        "MULTI-SPORT ANTHOLOGY",
        "ANIMATION - ADULT",
        "INSTRUCT/INFO - COOKING",
        "SERIES - ACTION/ADVENTURE",
        "COMEDY - OTHER",
        "GENERAL VARIETY",
        "INSTRUCT/INFO - ARTS & CRAFT",
        "INSTRUCT/INFO-LFSTYL/FSHN/HLTH",
        "MUSIC - VARIETY",
        "COMEDY - STAND UP",
        "MUSIC VIDEOS - MISCELLANEOUS",
        "COMEDY - SITUATION",
        "SERIES - REALITY",
        "CHILDREN - GAME SHOWS",
        "CHILDREN - MOVIES",
        "SERIES - WESTERN",
        "SUSPENSE MYSTERY",
        "Unknown",
        "DOCUMENTARY - SOCIETY",
        "FEATURE FILM",
        "INSTRUCT/INFO - TRAVEL",
        "INSTRUCT/INFO - OTHER",
        "DOCUMENTARY - SCIENCE/TECHNICA"
      ],
      // numEpisodes: {
      //   min: 1,
      //   max: 2603
      // },
      // duration: {
      //   min: 19.5,
      //   max: 390
      // },
      filteredNetwork: [],
      networkFilterText: "",
      network: [
        "WETV",
        "UNI",
        "NBAT",
        "FXX",
        "UMA",
        "CW",
        "WGNA",
        "MTV",
        "DSNY",
        "HBOM",
        "ABC",
        "RFD",
        "GAC",
        "CINL",
        "SCI",
        "CBS",
        "TNNK",
        "TWC",
        "HGTV",
        "NKTNS",
        "CNNE",
        "CMT",
        "BOOM",
        "ID",
        "FOOD",
        "CNN",
        "BTN",
        "COM",
        "UP",
        "AXS",
        "FOX",
        "DLIF",
        "RLZC",
        "IFC",
        "AEN",
        "CC",
        "DISJR",
        "GRT",
        "BET",
        "TRAV",
        "MYS",
        "TOON",
        "BRVO",
        "NBC",
        "ETV",
        "NICK",
        "DFC",
        "HMM",
        "DISC",
        "SUND",
        "TVL",
        "HALL",
        "MET",
        "NKJR",
        "DIY",
        "FYI",
        "LOGO",
        "FX",
        "PAR",
        "ESPN",
        "UKID",
        "MSNBC",
        "POP",
        "NGWD",
        "AHC",
        "NGM",
        "BHER",
        "DFAM",
        "MTVC",
        "AMC",
        "LMN",
        "DAM",
        "MAXP",
        "STZP",
        "HLDRM",
        "VH1",
        "ION",
        "LAF",
        "TLC",
        "GALA",
        "TV1",
        "SHO1",
        "OWN",
        "CNBC",
        "ESPN2",
        "TNT",
        "SYFY",
        "VICE",
        "HLN",
        "NAN",
        "ENCY",
        "MT",
        "REY",
        "LIF",
        "ENT",
        "APL",
        "FRFM",
        "BBCA",
        "FXM",
        "DSE",
        "TRU",
        "OVTN",
        "MTV2",
        "OXYG",
        "HIST",
        "AMTV",
        "ESC",
        "USA",
        "TBSC",
        "SMTH",
        "UNVSO",
        "INSP",
        "FUSE",
        "CMDY",
        "TEL",
        "BOU",
        "NFLN",
        "MLBN",
        "NGC",
        "DXD"
      ],
      demos: [],
      countySizes: [
        { name: "“A” county -25 largest metropolitan areas", value: 3 },
        {
          name: "“B” county -over 150,000 in population, but not an “A” county",
          value: 2
        },
        {
          name:
            "“C” county -over 40,000 in population, but not an “A” or “B” county",
          value: 1
        },
        { name: "“D” county -all others", value: 0 }
      ],
      educationLevels: [
        { name: "College Graduate (i.e., 4+ years of college)", value: 5 },
        { name: "Some college (i.e., 1-3 years of college)", value: 4 },
        { name: "High School graduate (i.e., 12 years)", value: 3 },
        { name: "Some High School (i.e., 9-11 years)", value: 2 },
        { name: "Grade school (i.e., 0-8 years)", value: 1 },
        { name: "Unknown", value: 0 }
      ],
      householdIncome: {
        min: 0,
        max: 500
      },
      householdLanguage: [
        "English Only",
        "Bilingual",
        "Mostly Spanish",
        "Spanish Only",
        "Mostly English"
      ],
      numberChildren: {
        min: 0,
        max: 9
      },
      numberAdults: {
        min: 1,
        max: 9
      },
      householdSize: [
        "single person household",
        "2 person household",
        "3 person household",
        "4 or more persons in the household"
      ],
      // hasCat, hasDog
      weeklyViewingMinutes: {
        min: 0,
        max: 14000
      }
    };
  },
  watch: {
    typeSummaryFilterText(val) {
      this.filteredTypeSummary = this.programTypeSummary
        .filter(pts => !val || pts.includes(val.toUpperCase()))
        .sort();
    },
    programTypeFilterText(val) {
      this.filteredProgramType = this.nhiProgramType
        .filter(pts => !val || pts.includes(val.toUpperCase()))
        .sort();
    },
    networkFilterText(val) {
      this.filteredNetwork = this.network
        .filter(pts => !val || pts.includes(val.toUpperCase()))
        .sort();
    }
  },
  methods: {
    filterTypeSummary() {}
  },
  computed: {
    ...mapState({})
  }
};
</script>
