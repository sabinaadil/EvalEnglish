<template>
    <div class="container mx-auto p-6">
        <h1 class="text-3xl font-bold mb-4">Проверка и оценка ответов</h1>
        <!-- Краткая информация о курсе -->
        <div v-if="course" class="mb-6 p-4 border rounded shadow bg-white">
            <h2 class="text-2xl font-semibold text-blue-800">{{ course.name }}</h2>
            <p class="text-gray-700">{{ course.description }}</p>
        </div>
        <!-- Таблица студентов -->
        <div v-if="students && students.length" class="bg-white rounded shadow overflow-x-auto">
            <table class="min-w-full">
                <thead>
                    <tr class="bg-gray-200">
                        <th class="px-4 py-2">Имя</th>
                        <th class="px-4 py-2">Email</th>
                        <th class="px-4 py-2">Дата регистрации</th>
                        <th class="px-4 py-2">Действие</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="student in students" :key="student.id" class="border-b hover:bg-gray-100">
                        <td class="px-4 py-2">{{ student.participant.first_name }} {{ student.participant.last_name }}
                        </td>
                        <td class="px-4 py-2">{{ student.participant.email }}</td>
                        <td class="px-4 py-2">{{ formatDate(student.enrolled_at) }}</td>
                        <td class="px-4 py-2">
                            <button @click="goToStudentReview(student)"
                                class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded">
                                Проверить ответы
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else class="text-gray-500">
            Студенты не найдены.
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "TeacherCourseAssessments",
    props: {
        courseId: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            course: null,
            students: [],
        };
    },
    created() {
        // Для отладки: выводим параметры роутера
        console.log("Параметры маршрута:", this.$route.params);
        // Если через роутер передается параметр, можно также использовать:
        // this.courseId = this.$route.params.courseId;
        this.fetchCourseDetails();
        this.fetchStudents();
    },
    methods: {
        async fetchCourseDetails() {
            try {
                const response = await axios.get(`/api/course-detail/${this.courseId}/`);
                this.course = response.data;
            } catch (error) {
                console.error("Ошибка загрузки курса:", error);
            }
        },
        async fetchStudents() {
            try {
                const response = await axios.get(`/api/course-participants/${this.courseId}/`);
                this.students = response.data;
            } catch (error) {
                console.error("Ошибка загрузки студентов:", error);
            }
        },
        formatDate(dateStr) {
            if (!dateStr) return "";
            return new Date(dateStr).toLocaleDateString();
        },
        goToStudentReview(studentRecord) {
            const userId = studentRecord.participant.id;
            console.log('ID студента:', userId);
            this.$router.push({
                name: "student-answer-review",
                params: { courseId: this.courseId, studentId: userId },
            });
        }
    },
};
</script>

<style scoped>
table {
    border-collapse: collapse;
    width: 100%;
}

th,
td {
    padding: 0.75rem;
    text-align: left;
}
</style>