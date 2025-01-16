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
      role: "student",
      isTeacher: false,
      isSuperuser: false,
    },
  }),

  actions: {
    initStore() {
      console.log("Initializing store");
      if (localStorage.getItem("user.access")) {
        this.user.access = localStorage.getItem("user.access");
        this.user.refresh = localStorage.getItem("user.refresh");
        this.user.id = localStorage.getItem("user.id");
        this.user.firstName = localStorage.getItem("user.firstName");
        this.user.lastName = localStorage.getItem("user.lastName");
        this.user.email = localStorage.getItem("user.email");
        this.user.avatar = localStorage.getItem("user.avatar");
        this.user.role = localStorage.getItem("user.role") || "student";
        this.user.isTeacher = localStorage.getItem("user.isTeacher") === "true";
        this.user.isSuperuser =
          localStorage.getItem("user.isSuperuser") === "true";

        this.user.isAuthenticated = true;
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.user.access}`;
        this.refreshToken();

        console.log("Initialized user:", { ...this.user });
      }
    },

    setToken(data) {
      this.user.access = data.access;
      this.user.refresh = data.refresh;
      this.user.isAuthenticated = true;

      localStorage.setItem("user.access", data.access);
      localStorage.setItem("user.refresh", data.refresh);
      axios.defaults.headers.common["Authorization"] = `Bearer ${data.access}`;
    },

    removeToken() {
      this.user.access = null;
      this.user.refresh = null;
      this.user.isAuthenticated = false;
      this.user.id = null;
      this.user.firstName = "";
      this.user.lastName = "";
      this.user.email = "";
      this.user.avatar = null;
      this.user.role = "student";
      this.user.isTeacher = false;
      this.user.isSuperuser = false;

      localStorage.removeItem("user.access");
      localStorage.removeItem("user.refresh");
      localStorage.removeItem("user.id");
      localStorage.removeItem("user.firstName");
      localStorage.removeItem("user.lastName");
      localStorage.removeItem("user.email");
      localStorage.removeItem("user.avatar");
      localStorage.removeItem("user.role");
      localStorage.removeItem("user.isTeacher");
      localStorage.removeItem("user.isSuperuser");

      delete axios.defaults.headers.common["Authorization"];
    },

    setUserInfo(user) {
      this.user.id = user.id;
      this.user.firstName = user.first_name;
      this.user.lastName = user.last_name;
      this.user.email = user.email;
      this.user.avatar = user.avatar;
      this.user.role = user.role || "student";
      this.user.isTeacher = user.is_teacher || false;
      this.user.isSuperuser = user.is_superuser || false;

      localStorage.setItem("user.id", user.id);
      localStorage.setItem("user.firstName", user.first_name);
      localStorage.setItem("user.lastName", user.last_name);
      localStorage.setItem("user.email", user.email);
      localStorage.setItem("user.avatar", user.avatar);
      localStorage.setItem("user.role", user.role || "student");
      localStorage.setItem(
        "user.isTeacher",
        user.is_teacher ? "true" : "false"
      );
      localStorage.setItem(
        "user.isSuperuser",
        user.is_superuser ? "true" : "false"
      );
    },

    refreshToken() {
      if (!this.user.refresh) {
        this.removeToken();
        return;
      }
      axios
        .post("/api/refresh/", { refresh: this.user.refresh })
        .then((response) => {
          this.user.access = response.data.access;
          localStorage.setItem("user.access", response.data.access);
          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${response.data.access}`;
        })
        .catch((error) => {
          console.error("Error refreshing token", error);
          this.removeToken();
        });
    },

    logout() {
      this.removeToken();
    },
  },
});
