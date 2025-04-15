<template>
    <div>
        <!-- Шапка с названием и основными данными о курсе -->
        <header class="bg-gray-800 text-white py-8 px-4 rounded-lg mb-6">
            <div class="container mx-auto">
                <h1 class="text-4xl font-bold mb-2">{{ course?.name }}</h1>
                <p class="text-lg mb-4">{{ courseSubtitle }}</p>
                <div class="flex flex-wrap items-center space-x-6 text-sm">
                    <div class="flex items-center space-x-2">
                        <span class="text-gray-200">
                            Мұғалім: {{ teacherName }}
                        </span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span class="text-gray-200">
                            {{ totalModulesCount }} модуль
                        </span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span class="text-gray-200">
                            {{ totalLessonsCount }} сабақтар
                        </span>
                    </div>
                </div>
            </div>
        </header>

        <!-- Основной контент -->
        <div class="container mx-auto px-4 md:px-0">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <!-- Левая часть: описание курса, "Не үйренесіз" и модули -->
                <div class="md:col-span-2">
                    <h2 class="text-2xl font-semibold mb-4">Курс сипаттамасы</h2>
                    <p class="text-gray-700 leading-relaxed">{{ course?.description }}</p>

                    <h3 class="text-xl font-semibold mt-8 mb-3">Не үйренесіз</h3>
                    <ul class="list-disc list-inside text-gray-700 space-y-1">
                        <li v-for="(item, index) in whatYouWillLearn" :key="index">
                            {{ item }}
                        </li>
                    </ul>

                    <h3 class="text-xl font-semibold mt-8 mb-3">Модульдер мен Сабақтар</h3>
                    <!-- Улучшенный аккордеон для модулей -->
                    <div v-for="(module, idx) in course?.modules" :key="module.id" class="mb-6">
                        <!-- Заголовок модуля -->
                        <div class="cursor-pointer bg-blue-50 hover:bg-blue-100 transition-all duration-200 p-4 rounded-lg flex justify-between items-center shadow"
                            @click="toggleModule(idx)">
                            <div>
                                <h4 class="text-xl font-bold text-gray-800">{{ module.title }}</h4>
                                <p class="text-sm text-gray-600 mt-1">
                                    {{ module.description }}
                                </p>
                            </div>
                            <!-- Иконка для раскрытия/сокрытия -->
                            <div>
                                <svg v-if="expandedModules[idx]" xmlns="http://www.w3.org/2000/svg"
                                    class="h-6 w-6 text-gray-500 transform rotate-180 transition-transform duration-200"
                                    viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd"
                                        d="M5.293 9.293a1 1 0 011.414 0L10 12.586l3.293-3.293a1 1 0 011.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                                        clip-rule="evenodd" />
                                </svg>
                                <svg v-else xmlns="http://www.w3.org/2000/svg"
                                    class="h-6 w-6 text-gray-500 transition-transform duration-200" viewBox="0 0 20 20"
                                    fill="currentColor">
                                    <path fill-rule="evenodd"
                                        d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                                        clip-rule="evenodd" />
                                </svg>
                            </div>
                        </div>

                        <!-- Содержимое модуля: уроки (аккордеон) -->
                        <transition name="fade">
                            <div v-show="expandedModules[idx]"
                                class="mt-2 bg-white border-l-4 border-blue-500 pl-4 py-3 rounded-lg shadow-sm">
                                <ul class="space-y-2">
                                    <li v-for="lesson in module.lessons" :key="lesson.id"
                                        class="flex items-center space-x-2 text-gray-700">
                                        <!-- Иконка урока -->
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-500"
                                            fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4" />
                                        </svg>
                                        <span>{{ lesson.title }}</span>
                                    </li>
                                </ul>
                            </div>
                        </transition>
                    </div>
                </div>

                <!-- Правая часть: кнопка записи/перехода и отписки -->
                <div class="bg-gray-50 rounded-lg p-6 shadow-lg h-fit self-start">
                    <button @click="enrollCourse"
                        class="w-full bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded transition-colors">
                        {{ enrolled ? "Оқуды бастау" : "Курсқа жазылу" }}
                    </button>
                    <!-- Если пользователь записан, показываем кнопку отписки -->
                    <div v-if="enrolled" class="mt-4 text-center">
                        <button @click="openUnsubscribeModal" class="text-red-500 underline">
                            Курстан бас тарту
                        </button>
                    </div>
                    <!-- Сообщение об успешной записи/отписке -->
                    <div v-if="enrollmentSuccessMessage" class="mt-4 text-center text-green-600 text-lg font-medium">
                        {{ enrollmentSuccessMessage }}
                    </div>
                </div>
            </div>
        </div>

        <!-- Модальное окно для подтверждения отписки -->
        <div v-if="showUnsubscribeModal"
            class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div class="bg-white p-6 rounded shadow max-w-sm w-full">
                <h3 class="text-xl font-bold mb-4 text-gray-800">Растау</h3>
                <p class="text-gray-700 mb-6">Сіз шынымен курстан бас тартқыңыз келе ме?</p>
                <div class="flex justify-end space-x-4">
                    <button @click="closeUnsubscribeModal" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">
                        Болдырмау
                    </button>
                    <button @click="confirmUnsubscribe"
                        class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600">
                        Растау
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "CourseDetailView",
    props: {
        courseId: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            course: null,                   // Данные о курсе
            loading: false,                 // Индикатор загрузки
            error: null,                    // Сообщение об ошибке
            expandedModules: [],            // Состояния аккордеона для модулей
            enrolled: false,                // Флаг подписки на курс
            enrollmentSuccessMessage: "",   // Сообщение об успешной записи/отписке
            showUnsubscribeModal: false,    // Флаг показа модального окна отписки
            whatYouWillLearn: [
                "Негізгі деңгейдегі тілдік қарым-қатынас дағдылары",
                "Дұрыс айтылу және фонетика",
                "Ағылшын тіліндегі негізгі уақыттар",
                "Оқу және жазу дағдылары"
            ],
        };
    },
    computed: {
        teacherName() {
            if (!this.course || !this.course.teacher) return "";
            const { first_name: firstName = "", last_name: lastName = "" } = this.course.teacher;
            return `${firstName} ${lastName}`.trim();
        },
        courseSubtitle() {
            return "Негізгі ағылшын курсы";
        },
        totalLessonsCount() {
            if (!this.course || !this.course.modules) return 0;
            return this.course.modules.reduce((total, module) => total + (module.lessons ? module.lessons.length : 0), 0);
        },
        totalModulesCount() {
            if (!this.course || !this.course.modules) return 0;
            return this.course.modules.length;
        }
    },
    mounted() {
        this.fetchCourseDetail();
    },
    methods: {
        async fetchCourseDetail() {
            this.loading = true;
            try {
                const response = await axios.get(`/api/course-detail/${this.courseId}/`);
                this.course = response.data;
                if (this.course.modules) {
                    this.expandedModules = this.course.modules.map(() => false);
                }
                // После загрузки курса проверяем, записан ли пользователь на этот курс
                if (this.course && this.course.id) {
                    this.fetchEnrollmentStatus();
                }
            } catch (err) {
                this.error = "Ошибка загрузки данных курса. Попробуйте позже.";
                console.error("Ошибка загрузки курса:", err);
            } finally {
                this.loading = false;
            }
        },
        // Метод для получения списка курсов пользователя и определения, записан ли текущий курс
        async fetchEnrollmentStatus() {
            try {
                const response = await axios.get("/api/my/courses/");
                // Предполагаем, что API возвращает массив курсов
                const myCourses = response.data;
                // Проверяем, содержит ли список курсов курс с текущим идентификатором
                if (myCourses.some(c => c.id === this.course.id)) {
                    this.enrolled = true;
                } else {
                    this.enrolled = false;
                }
            } catch (err) {
                console.error("Ошибка получения моих курсов:", err);
            }
        },
        toggleModule(index) {
            this.expandedModules[index] = !this.expandedModules[index];
        },
        async enrollCourse() {
            if (this.enrolled) {
                // Если пользователь уже записан, перенаправляем его на страницу курса
                this.$router.push({ name: "CoursePlay", params: { courseId: this.course.id } });
                return;
            }
            try {
                const response = await axios.post("/api/enroll/", { course: this.courseId });
                this.enrolled = true;
                this.enrollmentSuccessMessage = `Вы успешно подписались на курс "${this.course.name}"!`;
            } catch (err) {
                console.error("Ошибка при записи на курс:", err);
                alert("Не удалось записаться на курс. Попробуйте позже.");
            }
        },
        openUnsubscribeModal() {
            this.showUnsubscribeModal = true;
        },
        closeUnsubscribeModal() {
            this.showUnsubscribeModal = false;
        },
        async confirmUnsubscribe() {
            try {
                await axios.delete(`/api/course/${this.course.id}/leave/`);
                this.enrolled = false;
                this.enrollmentSuccessMessage = "Вы успешно отписались от курса!";
            } catch (err) {
                console.error("Ошибка отписки от курса:", err);
                alert("Не удалось отписаться от курса. Попробуйте позже.");
            } finally {
                this.closeUnsubscribeModal();
            }
        },
    },
};
</script>

<style scoped>
/* Плавный эффект для аккордеона */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>