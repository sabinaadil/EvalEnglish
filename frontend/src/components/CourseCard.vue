<template>
    <div class="relative bg-white rounded shadow hover:shadow-lg transition duration-300">
        <!-- Изображение курса (заглушка) -->
        <div class="h-40 bg-gray-200 flex items-center justify-center">
            <span class="text-gray-500 text-xs">Изображение курса</span>
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
                        Преподаватель: {{ course.teacher.first_name }} {{ course.teacher.last_name }}
                    </p>
                </div>
                <!-- Отображаем меню опций только если showOptions=true -->
                <div v-if="showOptions" class="relative" v-click-outside="closeMenu">
                    <button @click="toggleMenu" class="text-gray-600 hover:text-gray-800 focus:outline-none">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                            <path
                                d="M12 8a2 2 0 110-4 2 2 0 010 4zm0 2a2 2 0 110 4 2 2 0 010-4zm0 6a2 2 0 110 4 2 2 0 010-4z" />
                        </svg>
                    </button>
                    <div v-if="menuOpen"
                        class="absolute right-0 mt-2 w-40 bg-white border border-gray-200 rounded shadow-lg z-10">
                        <ul>
                            <li>
                                <button @click="editCourse"
                                    class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                    Редактировать
                                </button>

                            </li>
                            <li>
                                <button @click="deleteCourse"
                                    class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                    Удалить
                                </button>
                            </li>
                            <li>
                                <button @click="publishCourse"
                                    class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                    Опубликовать
                                </button>
                            </li>
                        </ul>
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
            required: true,
        },
        showOptions: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            menuOpen: false,
        };
    },
    methods: {
        toggleMenu() {
            this.menuOpen = !this.menuOpen;
        },
        closeMenu() {
            this.menuOpen = false;
        },
        async editCourse() {
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
            },
        },
    },
};
</script>

<style scoped>
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>