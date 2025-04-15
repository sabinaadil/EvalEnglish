<template>
    <!-- Если showOptions == false, оборачиваем карточку в router-link для навигации -->
    <router-link v-if="!showOptions" :to="{ name: 'course-detail', params: { courseId: course.id } }" class="block">
        <div class="relative bg-white rounded shadow hover:shadow-lg transition duration-300">
            <!-- Изображение курса -->
            <div class="h-40 flex items-center justify-center overflow-hidden rounded-t">
                <img :src="defaultImage" alt="Дефолтное изображение курса" class="object-cover w-full h-full" />
            </div>
            <div class="p-4">
                <div class="flex justify-between items-start">
                    <div>
                        <h2 class="text-lg font-semibold mb-2 line-clamp-2">
                            {{ course.name }}
                        </h2>
                        <p class="text-sm text-gray-600 line-clamp-3">
                            {{ course.description }}
                        </p>
                        <p class="text-xs text-gray-500 mt-2">
                            Оқытушы: {{ course.teacher.first_name }} {{ course.teacher.last_name }}
                        </p>
                    </div>
                    <!-- Если опции включены, отображаем меню (но при клике не происходит навигация) -->
                    <div v-if="showOptions" class="relative" v-click-outside="closeMenu">
                        <button @click.stop="toggleMenu" class="text-gray-600 hover:text-gray-800 focus:outline-none">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="currentColor"
                                viewBox="0 0 24 24">
                                <path
                                    d="M12 8a2 2 0 110-4 2 2 0 010 4zm0 2a2 2 0 110 4 2 2 0 010-4zm0 6a2 2 0 110 4 2 2 0 010-4z" />
                            </svg>
                        </button>
                        <div v-if="menuOpen"
                            class="absolute right-0 mt-2 w-40 bg-white border border-gray-200 rounded shadow-lg z-10">
                            <ul>
                                <li>
                                    <button @click.stop="editCourse"
                                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        Өңдеу
                                    </button>
                                </li>
                                <li>
                                    <button @click.stop="deleteCourse"
                                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        Жою
                                    </button>
                                </li>
                                <li>
                                    <button @click.stop="publishCourse"
                                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        Жариялау
                                    </button>
                                </li>
                                <!-- Новый пункт меню для проверки и оценки ответов -->
                                <li>
                                    <button @click.stop="checkAnswers"
                                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        Жауаптарды тексеру және бағалау
                                    </button>
                                </li>
                                <li>
                                    <button @click.stop="checkMetrics"
                                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        Аналитика
                                    </button>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </router-link>

    <!-- Если showOptions == true, выводим карточку без router-link (без навигации по клику на основную область) -->
    <div v-else class="block">
        <div class="relative bg-white rounded shadow hover:shadow-lg transition duration-300">
            <!-- Изображение курса -->
            <div class="h-40 flex items-center justify-center overflow-hidden rounded-t">
                <img :src="defaultImage" alt="Дефолтное изображение курса" class="object-cover w-full h-full" />
            </div>
            <div class="p-4">
                <div class="flex justify-between items-start">
                    <div>
                        <h2 class="text-lg font-semibold mb-2 line-clamp-2">
                            {{ course.name }}
                        </h2>
                        <p class="text-sm text-gray-600 line-clamp-3">
                            {{ course.description }}
                        </p>
                        <p class="text-xs text-gray-500 mt-2">
                            Оқытушы: {{ course.teacher.first_name }} {{ course.teacher.last_name }}
                        </p>
                    </div>
                    <!-- Меню опций -->
                    <div class="relative" v-click-outside="closeMenu">
                        <button @click.stop="toggleMenu" class="text-gray-600 hover:text-gray-800 focus:outline-none">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="currentColor"
                                viewBox="0 0 24 24">
                                <path
                                    d="M12 8a2 2 0 110-4 2 2 0 010 4zm0 2a2 2 0 110 4 2 2 0 010-4zm0 6a2 2 0 110 4 2 2 0 010-4z" />
                            </svg>
                        </button>
                        <div v-if="menuOpen"
                            class="absolute right-0 mt-2 w-40 bg-white border border-gray-200 rounded shadow-lg z-10">
                            <ul>
                                <li>
                                    <button @click.stop="editCourse"
                                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        Өңдеу
                                    </button>
                                </li>
                                <li>
                                    <button @click.stop="deleteCourse"
                                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        Жою
                                    </button>
                                </li>
                                <li>
                                    <button @click.stop="publishCourse"
                                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        Жариялау
                                    </button>
                                </li>
                                <!-- Новый пункт меню для проверки и оценки ответов -->
                                <li>
                                    <button @click.stop="checkAnswers"
                                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        Жауаптарды тексеру және бағалау
                                    </button>
                                </li>
                                <li>
                                    <button @click.stop="checkMetrics"
                                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        Аналитика
                                    </button>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
export default {
    name: "CourseCard",
    props: {
        course: {
            type: Object,
            required: true
        },
        showOptions: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            menuOpen: false,
            defaultImage: "/image.png"
        };
    },
    methods: {
        toggleMenu() {
            this.menuOpen = !this.menuOpen;
        },
        closeMenu() {
            this.menuOpen = false;
        },
        editCourse() {
            this.$router.push({ name: 'course-edit', params: { id: this.course.id } });
            this.menuOpen = false;
        },
        async deleteCourse() {
            if (!confirm("Вы уверены, что хотите удалить курс?")) return;
            try {
                await axios.delete(`/api/course/${this.course.id}/`);
                this.$emit("courseDeleted", this.course.id);
            } catch (error) {
                console.error("Ошибка удаления курса:", error);
            }
            this.menuOpen = false;
        },
        async publishCourse() {
            try {
                await axios.put(`/api/course/${this.course.id}/`, { is_published: true });
                this.$emit("coursePublished", this.course.id);
            } catch (error) {
                console.error("Ошибка публикации курса:", error);
            }
            this.menuOpen = false;
        },
        checkAnswers() {
            // Переход на страницу проверки и оценки ответов для курса.
            // Например, маршрут выглядит так: /teacher/course/:courseId/assessment
            this.$router.push({
                name: "teacher-course-assessment",
                params: { courseId: this.course.id }
            });
            this.menuOpen = false;
        },

        checkMetrics() {
            this.$router.push({
                name: "teacher-courses-analytics",
                params: { courseId: this.course.id }
            });
            this.menuOpen = false;
        }

    },
    directives: {
        clickOutside: {
            beforeMount(el, binding) {
                el.clickOutsideEvent = function (event) {
                    if (!(el === event.target || el.contains(event.target))) {
                        binding.value(event);
                    }
                };
                document.body.addEventListener("click", el.clickOutsideEvent);
            },
            unmounted(el) {
                document.body.removeEventListener("click", el.clickOutsideEvent);
            }
        }
    }
};
</script>

<style scoped>
/* Дополнительные стили можно добавить здесь */
</style>