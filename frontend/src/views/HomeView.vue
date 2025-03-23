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
                    <input type="text" placeholder="Название курса, автор или предмет"
                        class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition duration-200 ease-in-out shadow-sm" />
                </div>

                <!-- Выпадающий список -->
                <div class="relative">
                    <select
                        class="block appearance-none w-full bg-white border border-gray-300 rounded-lg px-3 py-2 pr-8 focus:outline-none focus:border-blue-500 transition duration-200 ease-in-out shadow-sm">
                        <option>На любом языке</option>
                        <option>На казахском</option>
                        <option>На русском</option>
                        <option>На узбекском</option>
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
                        <span class="ml-2 text-gray-700">С сертификатами</span>
                    </label>
                    <label class="inline-flex items-center">
                        <input type="checkbox" class="form-checkbox text-blue-600" />
                        <span class="ml-2 text-gray-700">Бесплатные</span>
                    </label>
                </div>

                <!-- Кнопка "Искать" -->
                <button
                    class="bg-blue-500 hover:bg-blue-600 text-white font-medium px-5 py-2 rounded-lg shadow transition duration-200 ease-in-out">
                    Искать
                </button>
            </div>
        </section>

        <!-- Вкладки (категории) -->
        <section class="mb-8">
            <ul class="flex justify-center space-x-4 text-gray-600 text-sm font-medium">
                <li class="cursor-pointer hover:text-gray-900 border-b-2 border-transparent hover:border-blue-600 pb-1">
                    В тренде
                </li>
                <li class="cursor-pointer hover:text-gray-900 border-b-2 border-transparent hover:border-blue-600 pb-1">
                    Новые курсы
                </li>
                <li class="cursor-pointer hover:text-gray-900 border-b-2 border-transparent hover:border-blue-600 pb-1">
                    Хиты EvalEnglish
                </li>
                <li class="cursor-pointer hover:text-gray-900 border-b-2 border-transparent hover:border-blue-600 pb-1">
                    Пакеты курсов
                </li>
                <li class="cursor-pointer hover:text-gray-900 border-b-2 border-transparent hover:border-blue-600 pb-1">
                    Актуальные скидки
                </li>
            </ul>
        </section>

        <!-- Раздел "Каталог курсов" -->
        <section>
            <h2 class="text-3xl font-bold text-center text-blue-800 mb-8">
                Каталог курсов
            </h2>
            <!-- Сетка карточек -->
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
                <CourseCard v-for="course in courses" :key="course.id" :course="course" />
            </div>
        </section>
    </div>
</template>


<script>
import { useUserStore } from "../stores/user";
import CourseCard from "../components/CourseCard.vue";

export default {
    name: "HomeView",
    components: {
        CourseCard,
    },
    data() {
        return {
            // Заглушки для курсов; потом замените на реальный запрос к API
            courses: [
                {
                    id: "1",
                    name: "Английский для начинающих",
                    description:
                        "Курс поможет вам освоить основы английского языка, начиная с алфавита и заканчивая простыми предложениями.",
                    teacher_name: "Иван Иванов",
                },
                {
                    id: "2",
                    name: "Продвинутый английский",
                    description:
                        "Курс рассчитан на тех, кто уже имеет базовые знания и хочет углубить свои навыки общения на английском.",
                    teacher_name: "Мария Петрова",
                },
                {
                    id: "3",
                    name: "Английский для путешествий",
                    description:
                        "Узнайте полезные фразы и лексику для комфортного путешествия по англоязычным странам.",
                    teacher_name: "Алексей Смирнов",
                },
                {
                    id: "4",
                    name: "Бизнес-английский",
                    description:
                        "Курс для тех, кто хочет улучшить навыки общения в деловой среде и вести переговоры на английском.",
                    teacher_name: "Елена Кузнецова",
                },
                {
                    id: "5",
                    name: "Бизнес-английский",
                    description:
                        "Курс для тех, кто хочет улучшить навыки общения в деловой среде и вести переговоры на английском.",
                    teacher_name: "Елена Кузнецова",
                },
                {
                    id: "6",
                    name: "Бизнес-английский",
                    description:
                        "Курс для тех, кто хочет улучшить навыки общения в деловой среде и вести переговоры на английском.",
                    teacher_name: "Елена Кузнецова",
                },
                {
                    id: "7",
                    name: "Бизнес-английский",
                    description:
                        "Курс для тех, кто хочет улучшить навыки общения в деловой среде и вести переговоры на английском.",
                    teacher_name: "Елена Кузнецова",
                },
                {
                    id: "8",
                    name: "Бизнес-английский",
                    description:
                        "Курс для тех, кто хочет улучшить навыки общения в деловой среде и вести переговоры на английском.",
                    teacher_name: "Елена Кузнецова",
                },

            ],
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
        }
    },
};
</script>

<style scoped>
/* Плавный hover на вкладках */
li {
    transition: border-color 0.3s;
}
</style>