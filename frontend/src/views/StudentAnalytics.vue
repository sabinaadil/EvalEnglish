<template>
    <div class="container mx-auto p-6">
        <h1 class="text-3xl font-bold mb-6 text-center">Сіздің үлгерім аналитикаңыз</h1>

        <!-- Фильтр по курсам -->
        <div class="mb-4 bg-white p-4 border rounded shadow">
            <label for="courseSelect" class="block text-gray-700 font-medium mb-2">
                Курсты таңдаңыз:
            </label>
            <select id="courseSelect" v-model="selectedCourseId" @change="onCourseChange"
                class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500">
                <option disabled value="">-- Курсты таңдаңыз --</option>
                <option v-for="course in courses" :key="course.id" :value="course.id">
                    {{ course.name }}
                </option>
            </select>
        </div>

        <!-- Блок аналитики (карточки) -->
        <div v-if="!loading && !error && metrics" class="mb-8 bg-white p-6 border rounded-lg shadow-lg">
            <h2 class="text-2xl font-semibold text-blue-800 mb-6 text-center">
                Аналитика көрсеткіштері
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <!-- Карточка: Заданий выполнено -->
                <div
                    class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition flex items-center justify-between">
                    <p class="text-gray-600 text-sm">Тапсырмалар орындалды</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.tasks_completed }}</p>
                </div>
                <!-- Карточка: Средний балл -->
                <div
                    class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition flex items-center justify-between">
                    <p class="text-gray-600 text-sm">Орташа балл</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.average_score }}</p>
                </div>
                <!-- Карточка: Оценка преподавателя -->
                <div
                    class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition flex items-center justify-between">
                    <p class="text-gray-600 text-sm">Оқытушы бағалауы</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.average_teacher_score }}</p>
                </div>
                <!-- Карточка: Оценка модели -->
                <div
                    class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition flex items-center justify-between">
                    <p class="text-gray-600 text-sm">Модель бағалауы</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.average_model_score }}</p>
                </div>
                <!-- Карточка: Время (сек.) -->
                <div
                    class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition flex items-center justify-between">
                    <p class="text-gray-600 text-sm">Уақыт (сек.)</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.time_spent }}</p>
                </div>
                <!-- Карточка: Попыток -->
                <div
                    class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition flex items-center justify-between">
                    <p class="text-gray-600 text-sm">Мүмкіндік</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.avg_attempts }}</p>
                </div>
                <!-- Карточка: Просрочено -->
                <div
                    class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition flex items-center justify-between">
                    <p class="text-gray-600 text-sm">Мерзімі өткен</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.late_submissions }}</p>
                </div>
                <!-- Карточка: Эффективность -->
                <div
                    class="p-4 bg-gray-50 border rounded-lg shadow hover:shadow-xl transition flex items-center justify-between">
                    <p class="text-gray-600 text-sm">Тиімділік</p>
                    <p class="text-2xl font-bold text-gray-800">{{ metrics.final_efficiency_score }}</p>
                </div>
            </div>
        </div>

        <!-- Блок графиков -->
        <div v-if="!loading && !error && metrics" class="bg-white p-6 border rounded-lg shadow-lg mt-8">
            <h2 class="text-2xl font-semibold text-blue-800 mb-4 text-center">Бағалау графиктері</h2>

            <!-- Две диаграммы в ряд -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="chart-container">
                    <canvas id="scoresBarChart"></canvas>
                </div>
                <div class="chart-container">
                    <canvas id="submissionDoughnutChart"></canvas>
                </div>
            </div>

            <!-- Радиальная диаграмма снизу -->
            <div class="mt-6">
                <div class="chart-container">
                    <canvas id="metricsRadarChart"></canvas>
                </div>
            </div>
        </div>

        <div v-else-if="loading" class="text-center text-gray-500">
            Загрузка аналитики...
        </div>
        <div v-else-if="error" class="text-center text-red-600">
            {{ error }}
        </div>
    </div>
</template>

<script>
import axios from "axios";
import Chart from "chart.js/auto";

export default {
    name: "StudentAnalytics",
    data() {
        return {
            courses: [],            // Курсы, в которых записан студент
            selectedCourseId: "",   // Выбранный ID курса
            metrics: null,          // Полученные аналитические данные
            loading: false,
            error: "",
            scoresBarChart: null,
            submissionDoughnutChart: null,
            metricsRadarChart: null,
        };
    },
    created() {
        this.fetchStudentCourses();
    },
    methods: {
        async fetchStudentCourses() {
            try {
                const response = await axios.get("/api/my/courses/");
                this.courses = response.data.results || response.data;
            } catch (err) {
                console.error("Ошибка загрузки курсов:", err);
                this.error = "Не удалось загрузить список курсов.";
            }
        },
        async onCourseChange() {
            await this.fetchMetrics();
        },
        async fetchMetrics() {
            this.loading = true;
            this.error = "";
            try {
                let url = "/api/activity-metrics/";
                if (this.selectedCourseId) {
                    url += `?course_id=${this.selectedCourseId}`;
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
        renderCharts() {
            if (this.scoresBarChart) this.scoresBarChart.destroy();
            if (this.submissionDoughnutChart) this.submissionDoughnutChart.destroy();
            if (this.metricsRadarChart) this.metricsRadarChart.destroy();

            // График 1: Столбчатая диаграмма оценок
            const scoresBarCtx = document.getElementById("scoresBarChart").getContext("2d");
            this.scoresBarChart = new Chart(scoresBarCtx, {
                type: "bar",
                data: {
                    labels: ["Орташа балл", "Оқытушы бағалауы", "Модель бағалауы"],
                    datasets: [{
                        label: "Бағалар",
                        data: [
                            this.metrics.average_score,
                            this.metrics.average_teacher_score,
                            this.metrics.average_model_score,
                        ],
                        backgroundColor: [
                            "rgba(75,192,192,0.6)",
                            "rgba(153,102,255,0.6)",
                            "rgba(255,159,64,0.6)",
                        ],
                        borderColor: [
                            "rgba(75,192,192,1)",
                            "rgba(153,102,255,1)",
                            "rgba(255,159,64,1)",
                        ],
                        borderWidth: 1,
                    }],
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true },
                    },
                    plugins: { legend: { display: false } },
                },
            });

            // График 2: Кольцевая диаграмма отправок (вовремя vs. просрочено)
            const onTime = this.metrics.tasks_completed - this.metrics.late_submissions;
            const submissionDoughnutCtx = document.getElementById("submissionDoughnutChart").getContext("2d");
            this.submissionDoughnutChart = new Chart(submissionDoughnutCtx, {
                type: "doughnut",
                data: {
                    labels: ["Уақытында", "Мерзімнен өткен"],
                    datasets: [{
                        data: [onTime, this.metrics.late_submissions],
                        backgroundColor: [
                            "rgba(54,162,235,0.6)",
                            "rgba(255,99,132,0.6)",
                        ],
                        borderColor: [
                            "rgba(54,162,235,1)",
                            "rgba(255,99,132,1)",
                        ],
                        borderWidth: 1,
                    }],
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: "bottom" } },
                },
            });

            // График 3: Радиальная диаграмма дополнительных показателей
            const metricsRadarCtx = document.getElementById("metricsRadarChart").getContext("2d");
            this.metricsRadarChart = new Chart(metricsRadarCtx, {
                type: "radar",
                data: {
                    labels: ["Тапсырмалар", "Уақыты", "Мүмкіндік", "Тиімділік"],
                    datasets: [{
                        label: "Көрсеткіштер",
                        data: [
                            this.metrics.tasks_completed,
                            this.metrics.time_spent,
                            this.metrics.avg_attempts,
                            this.metrics.final_efficiency_score,
                        ],
                        backgroundColor: "rgba(255,206,86,0.4)",
                        borderColor: "rgba(255,206,86,1)",
                        borderWidth: 1,
                    }],
                },
                options: {
                    responsive: true,
                    scales: { r: { beginAtZero: true } },
                    plugins: { legend: { position: "top" } },
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

.chart-container {
    height: 350px;
    /* При необходимости можно увеличить высоту */
}
</style>