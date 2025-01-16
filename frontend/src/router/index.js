import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import ProfileComponent from "../components/ProfileComponent.vue";
import TeacherApplicationView from "../views/TeacherApplicationView.vue";
import AdminNotificationsView from "../views/AdminNotificationsView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/signup",
      name: "signup",
      component: SignupView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/profile/:id",
      name: "profile",
      component: ProfileComponent,
      props: true,
      meta: { requiresAuth: true },
    },
    {
      path: "/teacher-application",
      name: "teacher-application",
      component: TeacherApplicationView,
      meta: { requiresAuth: true },
    },
    {
      path: "/admin/notifications",
      name: "admin-notifications",
      component: AdminNotificationsView,
      meta: { requiresAuth: true },
    },
  ],
});

export default router;
