import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import ProfileComponent from "../components/ProfileComponent.vue";
import TeacherApplicationView from "../views/TeacherApplicationView.vue";
import AdminNotificationsView from "../views/AdminNotificationsView.vue";
import NotificationView from "../views/NotificationView.vue";
import CreateCourse from "../views/CreateCourse.vue";
import CourseDetailView from "../views/CourseDetailView.vue"; // Импорт нового компонента
import CoursePlayView from "../views/CoursePlayView.vue";

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
    {
      path: "/notifications",
      name: "notifications",
      component: NotificationView,
    },
    {
      path: "/create-course",
      name: "create-course",
      component: CreateCourse,
    },
    // Новый маршрут для деталей курса
    {
      path: "/courses/:id",
      name: "course-detail",
      component: CourseDetailView,
      props: true,
    },
    {
      path: "/course-play/:id",
      name: "CoursePlay",
      component: CoursePlayView,
      props: (route) => ({ courseId: route.params.id }), // Вариант B
    },
  ],
});

export default router;
