import axios from "axios";
import { defineStore } from "pinia";

export const useUserStore = defineStore({
  id: "user",

  state: () => ({
    user: {
      isAuthenticated: false,
      id: null,
      firstName: "",
      lastName: "",
      email: "",
      access: null,
      refresh: null,
      avatar: null,
    },
  }),

  actions: {
    initStore() {
      console.log("initStore");
      if (localStorage.getItem("user.access")) {
        console.log("User has access!");
        this.user.access = localStorage.getItem("user.access");
        this.user.refresh = localStorage.getItem("user.refresh");
        this.user.id = localStorage.getItem("user.id");
        this.user.firstName = localStorage.getItem("user.firstName");
        this.user.lastName = localStorage.getItem("user.lastName");
        this.user.email = localStorage.getItem("user.email");
        this.user.avatar = localStorage.getItem("user.avatar");
        this.user.isAuthenticated = true;

        this.refreshToken();
        console.log("Initialized user:", {
          ...this.user,
        });
      }
    },

    setToken(data) {
      console.log("setToken", data);

      this.user.access = data.access;
      this.user.refresh = data.refresh;
      this.user.isAuthenticated = true;

      localStorage.setItem("user.access", data.access);
      localStorage.setItem("user.refresh", data.refresh);
    },

    removeToken() {
      console.log("removeToken");

      this.user.access = null;
      this.user.refresh = null;
      this.user.isAuthenticated = false;
      this.user.id = null;
      this.user.firstName = null;
      this.user.lastName = null;
      this.user.email = null;
      this.user.avatar = null;

      localStorage.setItem("user.access", "");
      localStorage.setItem("user.refresh", "");
      localStorage.setItem("user.id", "");
      localStorage.setItem("user.firstName", "");
      localStorage.setItem("user.lastName", "");
      localStorage.setItem("user.email", "");
      localStorage.setItem("user.avatar", "");

      console.log("Removed user:", this.user);
    },

    setUserInfo(user) {
      console.log("setUserInfo", user);

      this.user.id = user.id;
      this.user.firstName = user.first_name;
      this.user.lastName = user.last_name;
      this.user.email = user.email;
      this.user.avatar = user.avatar;

      localStorage.setItem("user.id", user.id);
      localStorage.setItem("user.firstName", user.firstName);
      localStorage.setItem("user.lastName", user.lastName);
      localStorage.setItem("user.email", user.email);
      localStorage.setItem("user.avatar", user.avatar);

      console.log("User", user);
    },

    refreshToken() {
      axios
        .post("/api/refresh/", {
          refresh: this.user.refresh,
        })
        .then((response) => {
          this.user.access = response.data.access;
          localStorage.setItem("user.access", response.data.access);

          axios.defaults.headers.common["Authorization"] =
            "Bearer " + response.data.access;
        })
        .catch((error) => {
          console.log(error);

          this.removeToken();
        });
    },
  },
});
