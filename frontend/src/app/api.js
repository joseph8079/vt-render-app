import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

export const api = axios.create({ baseURL: API_BASE_URL });

export function setAuthToken(token) {
  if (token) api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  else delete api.defaults.headers.common["Authorization"];
}

export async function login(username, password) {
  const { data } = await api.post("/auth/token/", { username, password });
  return data;
}
