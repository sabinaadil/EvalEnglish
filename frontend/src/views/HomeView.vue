<template>
    <div class="container mx-auto px-4">
        <!-- Блок поиска -->
        <section class="bg-gradient-to-r from-gray-100 to-gray-50 px-6 py-4 mb-8 rounded-lg shadow-md">
            <div class="flex flex-wrap items-center space-x-6">
                <!-- Поле поиска с иконкой -->
                <div class="relative flex-1">
                    <span class="absolute inset-y-0 left-0 flex items-center pl-3">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M10 4a6 6 0 1 1 0 12 6 6 0 0 1 0-12zM21 21l-4.35-4.35" />
                        </svg>
                    </span>
                    <input type="text" placeholder="Курстың атауы, авторы немесе пән"
                        class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition duration-200 ease-in-out shadow-sm" />
                </div>

                <!-- Выпадающий список -->
                <div class="relative">
                    <select
                        class="block appearance-none w-full bg-white border border-gray-300 rounded-lg px-3 py-2 pr-8 focus:outline-none focus:border-blue-500 transition duration-200 ease-in-out shadow-sm">
                        <option>Кез келген тілде</option>
                        <option>қазақ тілінде</option>
                        <option>Орыс тілінде</option>

                    </select>
                    <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-400">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
                        </svg>
                    </div>
                </div>

                <!-- Чекбоксы -->
                <div class="flex items-center space-x-4">
                    <label class="inline-flex items-center">
                        <input type="checkbox" class="form-checkbox text-blue-600" />
                        <span class="ml-2 text-gray-700">Сертификатымен</span>
                    </label>
                    <label class="inline-flex items-center">
                        <input type="checkbox" class="form-checkbox text-blue-600" />
                        <span class="ml-2 text-gray-700">Тегін</span>
                    </label>
                </div>

                <!-- Кнопка "Искать" -->
                <button
                    class="bg-blue-500 hover:bg-blue-600 text-white font-medium px-5 py-2 rounded-lg shadow transition duration-200 ease-in-out">
                    Іздеу
                </button>
            </div>
        </section>

        <!-- Вкладки (категории) -->
        <section class="mb-8">
            <ul class="flex justify-center space-x-4 text-gray-600 text-sm font-medium">
                <li class="cursor-pointer hover:text-gray-900 border-b-2 border-transparent hover:border-blue-600 pb-1">
                    Трендте
                </li>
                <li class="cursor-pointer hover:text-gray-900 border-b-2 border-transparent hover:border-blue-600 pb-1">
                    Жаңа курстар
                </li>
                <li class="cursor-pointer hover:text-gray-900 border-b-2 border-transparent hover:border-blue-600 pb-1">
                    EvalEnglish Хиттеры
                </li>
                <li class="cursor-pointer hover:text-gray-900 border-b-2 border-transparent hover:border-blue-600 pb-1">
                    Курс пакеттері
                </li>
                <li class="cursor-pointer hover:text-gray-900 border-b-2 border-transparent hover:border-blue-600 pb-1">
                    Ағымдағы науқандар
                </li>
            </ul>
        </section>

        <!-- Раздел "Каталог курсов" -->
        <section>
            <h2 class="text-3xl font-bold text-center text-blue-800 mb-8">
                Курстар каталогы
            </h2>
            <!-- Сетка карточек -->
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
                <CourseCard v-for="course in courses" :key="course.id" :course="course" />
            </div>
        </section>
    </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/user";
import CourseCard from "../components/CourseCard.vue";

export default {
    name: "HomeView",
    components: {
        CourseCard,
    },
    data() {
        return {
            courses: [],
        };
    },
    computed: {
        user() {
            const userStore = useUserStore();
            return userStore.user;
        },
    },
    created() {
        // Если пользователь не авторизован, перенаправляем на страницу логина
        if (!this.user.isAuthenticated) {
            this.$router.push({ name: "login" });
        } else {
            this.fetchCourses();
        }
    },
    methods: {
        async fetchCourses() {
            try {
                // Теперь делаем GET-запрос на /api/course/ (CourseAPIView)
                const response = await axios.get("/api/course/");
                // Пагинация DRF возвращает { count, next, previous, results }
                // Извлекаем массив курсов из поля results
                this.courses = response.data.results;
            } catch (error) {
                console.error("Ошибка получения курсов:", error);
            }
        },
    },
};
</script>

<style scoped>
/* Плавный hover на вкладках */
li {
    transition: border-color 0.3s;
}
</style>