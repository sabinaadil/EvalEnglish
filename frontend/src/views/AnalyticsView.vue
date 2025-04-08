<template>
    <div class="container mx-auto p-6">
        <h1 class="text-4xl font-bold text-blue-800 mb-6 text-center">
            Менің курстарым бойынша Аналитика
        </h1>
        <p class="text-lg text-gray-700 text-center mb-8">
            Бұл бетте әртүрлі ағылшын курстарының жалпы нәтижелері мен статистикасы көрсетіледі.
        </p>

        <!-- Негізгі көрсеткіштер -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div class="p-4 bg-white rounded-lg shadow text-center">
                <h3 class="text-xl font-semibold text-green-600">Орташа тапсырмалар саны</h3>
                <p class="text-2xl font-bold text-gray-800">{{ averageTasksCompleted }}</p>
            </div>
            <div class="p-4 bg-white rounded-lg shadow text-center">
                <h3 class="text-xl font-semibold text-green-600">Орташа балл</h3>
                <p class="text-2xl font-bold text-gray-800">{{ averageScore }}</p>
            </div>
            <div class="p-4 bg-white rounded-lg shadow text-center">
                <h3 class="text-xl font-semibold text-green-600">Орташа уақыт (мин)</h3>
                <p class="text-2xl font-bold text-gray-800">{{ averageTimeSpent }}</p>
            </div>
            <div class="p-4 bg-white rounded-lg shadow text-center">
                <h3 class="text-xl font-semibold text-green-600">Орташа тиімділік</h3>
                <p class="text-2xl font-bold text-gray-800">{{ averageFinalEfficiency }}</p>
            </div>
        </div>

        <!-- Графиктер -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
                <canvas ref="efficiencyChartRef"></canvas>
            </div>
            <div>
                <canvas ref="scoreChartRef"></canvas>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import {
    Chart,
    BarController,
    BarElement,
    CategoryScale,
    LinearScale,
    LineController,
    LineElement,
    PointElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';

Chart.register(
    BarController,
    BarElement,
    CategoryScale,
    LinearScale,
    LineController,
    LineElement,
    PointElement,
    Title,
    Tooltip,
    Legend
);

export default {
    name: 'AnalyticsView',
    setup() {
        // Үлгі аналитикалық деректер
        const analyticsData = ref([
            {
                id: "a1d1b1c1-d1e1-4a1f-a1b1-c1d1e1f1a1b1",
                activity_date: "2025-03-25",
                tasks_completed: 12,
                average_score: 0.78,
                average_teacher_score: 0.75,
                average_model_score: 0.81,
                time_spent: 520,
                avg_attempts: 1.3,
                late_submissions: 1,
                final_efficiency_score: 7.8,
                course_id: "course-101",
                course_name: "Ағылшын тілі: Бастапқы курсы",
                module_id: "module-201",
                user_email: "ali@mail.kz"
            },
            {
                id: "b2e2f2a2-a2b2-4b2c-b2a2-d2e2f2a2b2c2",
                activity_date: "2025-03-25",
                tasks_completed: 7,
                average_score: 0.65,
                average_teacher_score: 0.60,
                average_model_score: 0.68,
                time_spent: 430,
                avg_attempts: 2.1,
                late_submissions: 0,
                final_efficiency_score: 6.2,
                course_id: "course-102",
                course_name: "Ағылшын тілі: Орташа курсы",
                module_id: "module-202",
                user_email: "bolat@mail.kz"
            },
            {
                id: "c3f3a3b3-b3c3-4c3d-c3b3-e3f3a3b3c3d3",
                activity_date: "2025-03-25",
                tasks_completed: 15,
                average_score: 0.85,
                average_teacher_score: 0.88,
                average_model_score: 0.90,
                time_spent: 650,
                avg_attempts: 1.1,
                late_submissions: 2,
                final_efficiency_score: 9.1,
                course_id: "course-103",
                course_name: "Ағылшын тілі: Жетілдірілген курсы",
                module_id: "module-203",
                user_email: "diana@mail.kz"
            },
            {
                id: "d4a4b4c4-c4d4-4d4e-d4c4-f4a4b4c4d4e4",
                activity_date: "2025-03-25",
                tasks_completed: 5,
                average_score: 0.55,
                average_teacher_score: 0.50,
                average_model_score: 0.48,
                time_spent: 300,
                avg_attempts: 2.8,
                late_submissions: 3,
                final_efficiency_score: 4.7,
                course_id: "course-104",
                course_name: "Ағылшын тілі: Қосымша курсы",
                module_id: "module-204",
                user_email: "meruert@mail.kz"
            },
            {
                id: "e5b5c5d5-d5e5-4e5f-e5d5-a5b5c5d5e5f5",
                activity_date: "2025-03-25",
                tasks_completed: 10,
                average_score: 0.70,
                average_teacher_score: 0.65,
                average_model_score: 0.72,
                time_spent: 500,
                avg_attempts: 1.5,
                late_submissions: 0,
                final_efficiency_score: 7.1,
                course_id: "course-105",
                course_name: "Ағылшын тілі: Бастапқы курсы",
                module_id: "module-205",
                user_email: "serik@mail.kz"
            },
            {
                id: "f6c6d6e6-e6f6-4f6a-f6e6-b6c6d6e6f6a6",
                activity_date: "2025-03-25",
                tasks_completed: 8,
                average_score: 0.68,
                average_teacher_score: 0.63,
                average_model_score: 0.70,
                time_spent: 440,
                avg_attempts: 1.9,
                late_submissions: 1,
                final_efficiency_score: 6.6,
                course_id: "course-106",
                course_name: "Ағылшын тілі: Орташа курсы",
                module_id: "module-206",
                user_email: "ayagoz@mail.kz"
            },
            {
                id: "a7d7e7f7-f7a7-4a7b-a7f7-c7d7e7f7a7b7",
                activity_date: "2025-03-25",
                tasks_completed: 18,
                average_score: 0.92,
                average_teacher_score: 0.90,
                average_model_score: 0.95,
                time_spent: 720,
                avg_attempts: 1.2,
                late_submissions: 0,
                final_efficiency_score: 9.6,
                course_id: "course-107",
                course_name: "Ағылшын тілі: Жетілдірілген курсы",
                module_id: "module-207",
                user_email: "zhanar@mail.kz"
            },
            {
                id: "b8e8f8a8-a8b8-4b8c-b8a8-d8e8f8a8b8c8",
                activity_date: "2025-03-25",
                tasks_completed: 4,
                average_score: 0.50,
                average_teacher_score: 0.55,
                average_model_score: 0.52,
                time_spent: 280,
                avg_attempts: 3.2,
                late_submissions: 2,
                final_efficiency_score: 4.2,
                course_id: "course-108",
                course_name: "Ағылшын тілі: Қысқа курсы",
                module_id: "module-208",
                user_email: "asylbek@mail.kz"
            },
            {
                id: "c9f9a9b9-b9c9-4c9d-c9b9-e9f9a9b9c9d9",
                activity_date: "2025-03-25",
                tasks_completed: 11,
                average_score: 0.73,
                average_teacher_score: 0.70,
                average_model_score: 0.74,
                time_spent: 510,
                avg_attempts: 1.6,
                late_submissions: 0,
                final_efficiency_score: 7.4,
                course_id: "course-109",
                course_name: "Ағылшын тілі: Орташа курсы",
                module_id: "module-209",
                user_email: "nurgul@mail.kz"
            },
            {
                id: "d0a0b0c0-c0d0-4d0e-d0c0-f0a0b0c0d0e0",
                activity_date: "2025-03-25",
                tasks_completed: 9,
                average_score: 0.67,
                average_teacher_score: 0.66,
                average_model_score: 0.69,
                time_spent: 470,
                avg_attempts: 1.8,
                late_submissions: 1,
                final_efficiency_score: 6.8,
                course_id: "course-110",
                course_name: "Ағылшын тілі: Жетілдірілген курсы",
                module_id: "module-210",
                user_email: "murat@mail.kz"
            }
        ]);

        // Есептеулер:
        const averageTasksCompleted = computed(() => {
            const sum = analyticsData.value.reduce((acc, item) => acc + item.tasks_completed, 0);
            return (sum / analyticsData.value.length).toFixed(1);
        });

        const averageScore = computed(() => {
            const sum = analyticsData.value.reduce((acc, item) => acc + item.average_score, 0);
            return (sum / analyticsData.value.length).toFixed(2);
        });

        const averageTimeSpent = computed(() => {
            const sum = analyticsData.value.reduce((acc, item) => acc + item.time_spent, 0);
            return (sum / analyticsData.value.length / 60).toFixed(1);
        });

        const averageFinalEfficiency = computed(() => {
            const sum = analyticsData.value.reduce((acc, item) => acc + item.final_efficiency_score, 0);
            return (sum / analyticsData.value.length).toFixed(1);
        });

        // График деректері:
        const efficiencyLabels = computed(() => analyticsData.value.map(item => item.course_name));
        const efficiencyData = computed(() => analyticsData.value.map(item => item.final_efficiency_score));

        const scoreLabels = computed(() => analyticsData.value.map(item => item.user_email));
        const scoreData = computed(() => analyticsData.value.map(item => item.average_score));

        const efficiencyChartRef = ref(null);
        const scoreChartRef = ref(null);

        onMounted(() => {
            // Бар-чарт (тиімділік)
            new Chart(efficiencyChartRef.value, {
                type: 'bar',
                data: {
                    labels: efficiencyLabels.value,
                    datasets: [{
                        label: 'Тиімділік (баға)',
                        data: efficiencyData.value,
                        backgroundColor: 'rgba(34, 197, 94, 0.6)',
                        borderColor: 'rgba(34, 197, 94, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top'
                        },
                        title: {
                            display: true,
                            text: 'Курстар бойынша тиімділік'
                        }
                    }
                }
            });

            // Линейный график (студенттердің орташа баллы)
            new Chart(scoreChartRef.value, {
                type: 'line',
                data: {
                    labels: scoreLabels.value,
                    datasets: [{
                        label: 'Орташа балл',
                        data: scoreData.value,
                        fill: false,
                        borderColor: 'rgba(59, 130, 246, 1)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top'
                        },
                        title: {
                            display: true,
                            text: 'Студенттердің орташа баллы'
                        }
                    }
                }
            });
        });

        return {
            analyticsData,
            averageTasksCompleted,
            averageScore,
            averageTimeSpent,
            averageFinalEfficiency,
            efficiencyChartRef,
            scoreChartRef,
            efficiencyLabels,
            efficiencyData,
            scoreLabels,
            scoreData
        };
    }
};
</script>

<style scoped>
canvas {
    max-width: 100%;
}
</style>