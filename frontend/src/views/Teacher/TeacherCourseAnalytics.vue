<template>
    <div class="container mx-auto p-6">
        <h1 class="text-3xl font-bold mb-6 text-center">Студенттердің үлгерімін талдау</h1>

        <!-- Фильтр по курсам -->
        <div class="mb-4 bg-white p-4 border rounded shadow">
            <label for="courseSelect" class="block text-gray-700 font-medium mb-2">
                Курсты таңдаңыз:
            </label>
            <select id="courseSelect" v-model="selectedCourseId" @change="onCourseChange"
                class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500">
                <!-- Вариант "Все курсы" -->
                <option value="">Барлық курстар</option>
                <option v-for="course in courses" :key="course.id" :value="course.id">
                    {{ course.name }}
                </option>
            </select>
        </div>

        <!-- Фильтр по студентам (отображается, если выбран конкретный курс) -->
        <div v-if="selectedCourseId && students.length" class="mb-4 bg-white p-4 border rounded shadow">
            <label for="studentSelect" class="block text-gray-700 font-medium mb-2">
                Студентті таңдаңыз:
            </label>
            <select id="studentSelect" v-model="selectedStudentId" @change="onStudentChange"
                class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500">
                <!-- Вариант "Все студенты" -->
                <option value="">Барлық студенттер</option>
                <option v-for="participant in students" :key="participant.id" :value="participant.participant.id">
                    {{ participant.participant.first_name }} {{ participant.participant.last_name }}
                </option>
            </select>
        </div>

        <!-- Кнопка сброса фильтров -->
        <div class="mb-4 text-center">
            <button @click="resetFilters" class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">
                Сүзгілерді қалпына келтіріңіз
            </button>
        </div>

        <!-- Блок аналитики -->
        <div v-if="!loading && !error && metrics" class="mb-8 bg-white p-6 border rounded-lg shadow-lg">
            <h2 class="text-2xl font-semibold text-blue-800 mb-6 text-center">
                Аналитика көрсеткіштері
            </h2>
            <!-- Сетка карточек для каждого показателя -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <!-- Карточка: Заданий выполнено -->
                <div class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition">
                    <p class="text-gray-600 text-sm">Тапсырмалар орындалды</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.tasks_completed }}</p>
                </div>
                <!-- Карточка: Средний балл -->
                <div class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition">
                    <p class="text-gray-600 text-sm">Орташа балл</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.average_score }}</p>
                </div>
                <!-- Карточка: Оценка преподавателя -->
                <div class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition">
                    <p class="text-gray-600 text-sm">Оқытушы бағалауы</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.average_teacher_score }}</p>
                </div>
                <!-- Карточка: Оценка модели -->
                <div class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition">
                    <p class="text-gray-600 text-sm">Модель бағалауы</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.average_model_score }}</p>
                </div>
                <!-- Карточка: Время (сек.) -->
                <div class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition">
                    <p class="text-gray-600 text-sm">Уақыт (сек.)</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.time_spent }}</p>
                </div>
                <!-- Карточка: Әрекеттердің орташа саны -->
                <div class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition">
                    <p class="text-gray-600 text-sm">Әрекеттердің орташа саны</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.avg_attempts }}</p>
                </div>
                <!-- Карточка: Просроченные отправки -->
                <div class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition">
                    <p class="text-gray-600 text-sm">Мерзімі өткен жөнелтілімдер</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.late_submissions }}</p>
                </div>
                <!-- Карточка: Итоговая эффективность -->
                <div class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition">
                    <p class="text-gray-600 text-sm">Қорытынды тиімділік</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.final_efficiency_score }}</p>
                </div>
            </div>
        </div>
        <!-- Сообщения об ошибках или загрузке -->
        <div v-else-if="loading" class="text-center text-gray-500">
            Загрузка аналитики...
        </div>
        <div v-else-if="error" class="text-center text-red-600">
            {{ error }}
        </div>


        <!-- Графики -->
        <div v-if="!loading && !error && metrics" class="bg-white p-6 border rounded-lg shadow-lg">
            <h2 class="text-2xl font-semibold text-blue-800 mb-4 text-center">Бағалау графиктері</h2>
            <!-- Столбчатая диаграмма -->
            <div class="mb-8">
                <canvas id="scoresChart"></canvas>
            </div>
            <!-- Линейный график -->
            <div>
                <canvas id="attemptsChart"></canvas>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import Chart from "chart.js/auto";

export default {
    name: "TeacherCourseAnalytics",
    data() {
        return {
            courses: [],              // Список курсов преподавателя
            students: [],             // Список участников выбранного курса
            selectedCourseId: "",     // Выбранный ID курса, если пусто — все курсы
            selectedStudentId: "",    // Выбранный ID студента, если пусто — все студенты
            metrics: null,            // Аналитические данные
            loading: false,
            error: "",
            scoresChart: null,
            attemptsChart: null,
        };
    },
    created() {
        this.fetchTeacherCourses();
        // При отсутствии фильтров сразу запрашиваем сводные данные
        this.fetchMetrics();
    },
    methods: {
        async fetchTeacherCourses() {
            try {
                const response = await axios.get("/api/my/courses/");
                // Ожидаем, что API возвращает поле results или данные напрямую:
                this.courses = response.data.results || response.data;
            } catch (err) {
                console.error("Ошибка загрузки курсов:", err);
                this.error = "Не удалось загрузить список курсов.";
            }
        },
        async onCourseChange() {
            // Если выбран конкретный курс, загружаем список студентов по нему; иначе очищаем список
            if (this.selectedCourseId) {
                await this.fetchStudents();
            } else {
                this.students = [];
                this.selectedStudentId = "";
            }
            await this.fetchMetrics();
        },
        async onStudentChange() {
            await this.fetchMetrics();
        },
        async fetchStudents() {
            try {
                const response = await axios.get(`/api/course-participants/${this.selectedCourseId}/`);
                this.students = response.data;
            } catch (error) {
                console.error("Ошибка загрузки студентов:", error);
            }
        },
        async fetchMetrics() {
            this.loading = true;
            this.error = "";
            try {
                // Формируем URL с учетом наличия фильтров. Если фильтр не установлен — соответствующий параметр не добавляем.
                let url = "/api/activity-metrics/";
                let queryParams = [];
                if (this.selectedCourseId) {
                    queryParams.push(`course_id=${this.selectedCourseId}`);
                }
                if (this.selectedStudentId) {
                    queryParams.push(`student_id=${this.selectedStudentId}`);
                }
                if (queryParams.length > 0) {
                    url += "?" + queryParams.join("&");
                }
                console.log("Запрашиваем URL метрик:", url);
                const response = await axios.get(url);
                this.metrics = response.data;
                this.loading = false;
                this.$nextTick(() => {
                    this.renderCharts();
                });
            } catch (err) {
                console.error("Ошибка загрузки аналитики:", err);
                this.error = "Ошибка загрузки аналитики. Попробуйте позже.";
                this.loading = false;
            }
        },
        resetFilters() {
            // Сброс фильтров: все курсы и все студенты
            this.selectedCourseId = "";
            this.selectedStudentId = "";
            this.students = [];
            this.fetchMetrics();
        },
        renderCharts() {
            const scoresCanvas = document.getElementById("scoresChart");
            const attemptsCanvas = document.getElementById("attemptsChart");
            if (!scoresCanvas || !attemptsCanvas) {
                console.error("Элементы canvas не найдены.");
                return;
            }
            if (this.scoresChart) this.scoresChart.destroy();
            if (this.attemptsChart) this.attemptsChart.destroy();

            // Столбчатая диаграмма для оценок
            this.scoresChart = new Chart(scoresCanvas.getContext("2d"), {
                type: "bar",
                data: {
                    labels: ["Орташа балл", "Оқытушы бағалауы", "Модель бағалауы"],
                    datasets: [{
                        label: "Оценки",
                        data: [
                            this.metrics.average_score,
                            this.metrics.average_teacher_score,
                            this.metrics.average_model_score,
                        ],
                        backgroundColor: [
                            "rgba(75, 192, 192, 0.6)",
                            "rgba(153, 102, 255, 0.6)",
                            "rgba(255, 159, 64, 0.6)",
                        ],
                        borderColor: [
                            "rgba(75, 192, 192, 1)",
                            "rgba(153, 102, 255, 1)",
                            "rgba(255, 159, 64, 1)",
                        ],
                        borderWidth: 1,
                    }],
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 1,
                            ticks: {
                                callback: (value) => value.toFixed(1),
                            },
                        },
                    },
                    plugins: {
                        legend: {
                            display: false,
                        },
                    },
                },
            });

            // Линейный график для показателей попыток, времени и просрочки
            this.attemptsChart = new Chart(attemptsCanvas.getContext("2d"), {
                type: "line",
                data: {
                    labels: ["Орташа әрекет", "Жалпы уақыт", "Мерзімі өткен мүмкіндіктер"],
                    datasets: [{
                        label: "Показатели",
                        data: [
                            this.metrics.avg_attempts,
                            this.metrics.time_spent,
                            this.metrics.late_submissions,
                        ],
                        backgroundColor: "rgba(54, 162, 235, 0.6)",
                        borderColor: "rgba(54, 162, 235, 1)",
                        fill: false,
                        tension: 0.1,
                    }],
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                        },
                    },
                    plugins: {
                        legend: {
                            display: false,
                        },
                    },
                },
            });
        },
    },
};
</script>

<style scoped>
.container {
    max-width: 800px;
}
</style>