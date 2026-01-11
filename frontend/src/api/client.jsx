import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL;

export const api = axios.create({ baseURL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err?.response?.status === 401) {
      // optional: redirect to login
      // window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

