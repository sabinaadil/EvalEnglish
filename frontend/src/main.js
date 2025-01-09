import "./assets/main.css";
import axios from "axios";
import { createPinia } from "pinia";
import { createApp } from "vue";

import App from "./App.vue";
import router from "./router";

axios.defaults.baseURL = "http://127.0.0.1:8000";

const app = createApp(App);

app.use(createPinia());
app.use(router);

import { useUserStore } from "./stores/user";

const userStore = useUserStore();

userStore.initStore();

axios.interceptors.request.use(
  (config) => {
    if (userStore.activeLibrary) {
      config.headers["Active-Library"] = userStore.activeLibrary.id;
    }
    if (userStore.user.access) {
      config.headers["Authorization"] = `Bearer ${userStore.user.access}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

app.mount("#app");
