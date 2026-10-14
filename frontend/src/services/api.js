import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getHealth = async () => {
  const response = await API.get("/health");
  return response.data;
};

export const getAlerts = async () => {
  const response = await API.get("/alerts");
  return response.data;
};

export default API;