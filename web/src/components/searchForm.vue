<template>
  <div>
    <v-form ref="form" v-model="valid">
      <v-btn class="mr-4" @click="submit">
        submit
      </v-btn>
      <v-list expand dense>
        <v-list-group :value="expanded.model" dense>
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title>Model</v-list-item-title>
            </v-list-item-content>
          </template>
          <v-switch
            label="Use Nested Model"
            v-model="form.useNestedModel"
            class="mx-4"
            dense
          ></v-switch>
          <v-switch
            label="Use Degree Correction"
            v-model="form.useDegreeCorrection"
            class="mx-4"
            dense
          ></v-switch>
          <v-switch
            label="Use Edge Weights"
            v-model="form.useEdgeWeights"
            class="mx-4"
            dense
          ></v-switch>
          <v-text-field
            label="Sample Size"
            v-model="form.sampleSize"
            class="mx-4"
            type="number"
            dense
          ></v-text-field>
        </v-list-group>
        <v-list-group :value="expanded.content" dense>
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title>Content</v-list-item-title>
            </v-list-item-content>
          </template>
          <v-text-field
            label="Program Name"
            v-model="form.programName"
            class="mx-4"
            dense
            multiple
          ></v-text-field>
          <v-select
            label="Program Category"
            v-model="form.programCategory"
            class="mx-4"
            :items="programCategories"
            :clearable="true"
            dense
          ></v-select>
          <v-autocomplete
            label="Program Type Summary"
            v-model="form.programTypeSummary"
            class="mx-4"
            :items="filteredTypeSummary"
            :clearable="true"
            :search-input.sync="typeSummaryFilterText"
            dense
            multiple
          ></v-autocomplete>
          <v-autocomplete
            label="Program Type"
            v-model="form.programType"
            class="mx-4"
            :items="filteredProgramType"
            :clearable="true"
            :search-input.sync="programTypeFilterText"
            dense
            multiple
          ></v-autocomplete>
          <v-autocomplete
            label="Network"
            v-model="form.network"
            class="mx-4"
            :items="filteredNetwork"
            :clearable="true"
            :search-input.sync="networkFilterText"
            dense
            multiple
          ></v-autocomplete>
        </v-list-group>
        <v-list-group :value="expanded.viewers" dense>
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title>Viewers</v-list-item-title>
            </v-list-item-content>
          </template>
          <v-select
            label="Gender"
            v-model="form.gender"
            class="mx-4 my-0"
            :items="gender"
            :clearable="true"
            dense
          ></v-select>
          <div class="rangeSlider mx-4">
            <v-label>Age</v-label>
            <div class="rangeSliderInput">
              <v-checkbox v-model="form.useAge" class="my-0" dense></v-checkbox>
              <v-range-slider
                :disabled="!form.useAge"
                v-model="form.age"
                :thumb-size="24"
                thumb-label="always"
                :max="age.max"
                :min="age.min"
                dense
                class="my-0"
              ></v-range-slider>
            </div>
          </div>
          <div class="rangeSlider mx-4">
            <v-label>Income</v-label>
            <div class="rangeSliderInput">
              <v-checkbox
                v-model="form.useIncome"
                class="my-0"
                dense
              ></v-checkbox>
              <v-range-slider
                :disabled="!form.useIncome"
                v-model="form.income"
                :thumb-size="24"
                thumb-label="always"
                :max="income.max"
                :min="income.min"
                dense
                class="my-0"
              ></v-range-slider>
            </div>
          </div>
          <div class="rangeSlider mx-4">
            <v-label>Number of Children</v-label>
            <div class="rangeSliderInput">
              <v-checkbox
                v-model="form.useChildren"
                class="my-0"
                dense
              ></v-checkbox>
              <v-range-slider
                :disabled="!form.useChildren"
                v-model="form.children"
                :thumb-size="24"
                thumb-label="always"
                :max="children.max"
                :min="children.min"
                dense
                class="my-0"
              ></v-range-slider>
            </div>
          </div>
          <div class="rangeSlider mx-4">
            <v-label>Number of Adults</v-label>
            <div class="rangeSliderInput">
              <v-checkbox
                v-model="form.useAdults"
                class="my-0"
                dense
              ></v-checkbox>
              <v-range-slider
                :disabled="!form.useAdults"
                v-model="form.adults"
                :thumb-size="24"
                thumb-label="always"
                :max="adults.max"
                :min="adults.min"
                dense
                class="my-0"
              ></v-range-slider>
            </div>
          </div>
          <div class="rangeSlider mx-4">
            <v-label>Weekly Viewing Minutes</v-label>
            <div class="rangeSliderInput">
              <v-checkbox
                v-model="form.useViewingMinutes"
                class="my-0"
                dense
              ></v-checkbox>
              <v-range-slider
                :disabled="!form.useViewingMinutes"
                v-model="form.viewingMinutes"
                thumb-label="always"
                :max="weeklyViewingMinutes.max"
                :min="weeklyViewingMinutes.min"
                dense
                class="my-0"
              ></v-range-slider>
            </div>
          </div>
          <v-select
            :style="{ marginTop: '0 !important' }"
            label="County Size"
            v-model="form.countySize"
            class="mx-4"
            :items="countySizes"
            :clearable="true"
            item-text="name"
            item-value="value"
            dense
          ></v-select>
          <v-select
            label="Education Level"
            v-model="form.educationLevel"
            class="mx-4"
            :items="educationLevels"
            :clearable="true"
            item-text="name"
            item-value="value"
            dense
          ></v-select>
          <v-select
            label="Language"
            v-model="form.language"
            class="mx-4"
            :items="householdLanguage"
            :clearable="true"
            dense
          ></v-select>
          <v-select
            label="Household Size"
            v-model="form.size"
            class="mx-4"
            :items="householdSize"
            :clearable="true"
            :style="{ marginTop: '0 !important' }"
            dense
          ></v-select>
          <v-checkbox
            label="Has Cat"
            v-model="form.hasCat"
            class="mx-4 my-0"
            dense
          ></v-checkbox>
          <v-checkbox
            label="Has Dog"
            v-model="form.hasDog"
            class="mx-4 my-0"
            dense
          ></v-checkbox>
        </v-list-group>
      </v-list>
    </v-form>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { getResults } from "../services/api";

export default {
  name: "SearchForm",
  data() {
    return {
      valid: true,
      expanded: {
        model: false,
        content: false,
        viewers: true
      },
      form: {
        useNestedModel: true,
        useDegreeCorrection: true,
        useEdgeWeights: false,
        sampleSize: 250,
        programName: [],
        programCategory: "",
        programTypeSummary: [],
        programType: [],
        network: [],
        gender: "",
        useAge: false,
        age: [2, 99],
        useIncome: false,
        income: [0, 500],
        useChildren: false,
        children: [0, 9],
        useAdults: false,
        adults: [1, 9],
        countySize: null,
        educationLevel: null,
        language: "",
        useViewingMinutes: false,
        viewingMinutes: [0, 14000],
        size: "",
        hasCat: false,
        hasDog: false
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
      gender: ["Male", "Female"],
      age: {
        min: 2,
        max: 99
      },
      countySizes: [
        { name: "“A” county -25 largest metropolitan areas", value: 3 },
        {
          name: "“B” county -over 150,000 in population, but not “A”",
          value: 2
        },
        {
          name: "“C” county -over 40,000 in population, but not “A” or “B”",
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
      income: {
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
      children: {
        min: 0,
        max: 9
      },
      adults: {
        min: 1,
        max: 9
      },
      householdSize: [
        "single person household",
        "2 person household",
        "3 person household",
        "4 or more persons in the household"
      ],
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
    submit() {
      getResults(this.form);
    }
  },
  computed: {
    ...mapState({})
  }
};
</script>
<style scoped>
.rangeSliderInput {
  display: flex;
}
.rangeSlider .v-input {
  margin-top: 0;
}
.rangeSlider label {
  margin-top: 8px;
}
</style>
