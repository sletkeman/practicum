import axios from "axios";

axios.defaults.baseURL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8080/api/"
    : "/api/";

const fetchAllergens = () => axios.get("/allergens");

export { fetchAllergens };
