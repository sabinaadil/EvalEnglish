import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import ProfileComponent from "../components/ProfileComponent.vue";
import TeacherApplicationView from "../views/TeacherApplicationView.vue";
import AdminNotificationsView from "../views/AdminNotificationsView.vue";
import NotificationView from "../views/NotificationView.vue";
import CreateCourse from "../views/CreateCourse.vue";
import CourseDetailView from "../views/CourseDetailView.vue";
import CoursePlayView from "../views/CoursePlayView.vue";
import MyCourses from "../views/Teacher/MyCourses.vue";
import CourseEditView from "../views/Teacher/CourseEditView.vue";
import AnalyticsView from "../views/AnalyticsView.vue";
import TeacherCourseAssessments from "../views/Teacher/TeacherCourseAssessments.vue";
import StudentAnswerReview from "../views/Teacher/StudentAnswerReview.vue";
import TeacherCourseAnalytics from "../views/Teacher/TeacherCourseAnalytics.vue";
import StudentAnalytics from "../views/StudentAnalytics.vue";
import StudentMyCourses from "../views/StudentMyCourses.vue";

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
      path: "/teacher/courses",
      name: "teacher-courses",
      component: MyCourses,
    },
    {
      path: "/student/courses",
      name: "student-courses",
      component: StudentMyCourses,
    },
    {
      // Для страницы деталей курса используем параметр courseId
      path: "/course-detail/:courseId",
      name: "course-detail",
      component: CourseDetailView,
      props: true,
    },
    {
      // Меняем путь на единообразное именование параметра (courseId)
      path: "/course-play/:courseId",
      name: "CoursePlay",
      component: CoursePlayView,
      props: true,
    },
    {
      path: "/course/edit/:id",
      name: "course-edit",
      component: CourseEditView,
      props: true, // Это автоматически передаст параметр id как пропс в компонент
    },
    {
      path: "/analytics",
      name: "analytics",
      component: AnalyticsView,
      props: true,
    },
    {
      path: "/teacher/course/:courseId/assessment",
      name: "teacher-course-assessment",
      component: TeacherCourseAssessments,
      meta: { requiresAuth: true },
      // Если требуется передавать роутер параметры как пропсы:
      props: true,
    },
    {
      path: "/teacher/course/:courseId/assessment/:studentId",
      name: "student-answer-review",
      component: StudentAnswerReview,
      meta: { requiresAuth: true },
      props: true,
    },
    {
      path: "/teacher/courses/analytics",
      name: "teacher-courses-analytics",
      component: TeacherCourseAnalytics,
      meta: { requiresAuth: true },
    },
    {
      path: "/student/courses/analytics",
      name: "student-courses-analytics",
      component: StudentAnalytics,
      meta: { requiresAuth: true },
    },
  ],
});

export default router;
