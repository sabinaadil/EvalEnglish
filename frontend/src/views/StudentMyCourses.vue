<template>
    <div class="container mx-auto p-6">
        <h1 class="text-3xl font-bold mb-8 text-center text-gray-800">Менің курстарым</h1>

        <!-- Загрузка данных -->
        <div v-if="loading" class="text-center py-12">
            <p class="text-gray-500 text-lg">Жүктелуде...</p>
        </div>

        <!-- Если курсы получены -->
        <div v-else-if="courses.length">
            <h2 class="text-xl font-semibold mb-6 text-gray-700 text-center">Сіздің ағымдағы курстар тізімі</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <CourseCard v-for="course in courses" :key="course.id" :course="course || {}" class="course-card" />
            </div>
        </div>

        <!-- Если курсы отсутствуют -->
        <div v-else class="text-center py-12">
            <p class="text-gray-500 text-lg">Курстар табылмады 😔</p>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import CourseCard from "../components/CourseCard.vue";

export default {
    name: "StudentMyCourses",
    components: {
        CourseCard,
    },
    data() {
        return {
            courses: [],
            loading: true,
            error: null
        };
    },
    created() {
        this.fetchCourses();
    },
    methods: {
        async fetchCourses() {
            try {
                this.loading = true;
                const response = await axios.get("/api/my/courses/");
                this.courses = response.data.results || response.data || [];
            } catch (error) {
                console.error("Ошибка получения курсов:", error);
                this.error = error;
            } finally {
                this.loading = false;
            }
        },
    },
};
</script>

<style scoped>
.container {
    max-width: 1200px;
}

.course-card {
    min-width: 320px;
}
</style>