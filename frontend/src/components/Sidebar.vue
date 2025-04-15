<template>
    <div class="bg-gray-900 text-white w-80 flex-none p-4 overflow-auto rounded-lg">
        <div v-for="module in modules" :key="module.id" class="mb-6">
            <h3 class="text-lg font-semibold mb-2">{{ module.title }}</h3>
            <ul class="space-y-1">
                <li v-for="lesson in module.lessons" :key="lesson.id"
                    class="cursor-pointer px-2 py-1 rounded flex items-center transition-colors duration-200" :class="{
                        'bg-gray-700': lesson.id === currentLessonId,
                        'hover:bg-gray-700': lesson.id !== currentLessonId
                    }" @click="selectLesson(lesson)">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                    {{ lesson.title }}
                </li>
                <!-- Если у модуля есть контрольные вопросы, показываем дополнительный пункт -->
                <li v-if="module.questions && module.questions.length"
                    class="cursor-pointer px-2 py-1 rounded flex items-center transition-colors duration-200 bg-gray-600 hover:bg-gray-700"
                    @click="selectControlQuestions(module)">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01" />
                    </svg>
                    Қорытынды сұрақтар
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    name: "Sidebar",
    props: {
        modules: {
            type: Array,
            required: true,
        },
        currentLessonId: {
            type: [Number, String],
            default: null,
        },
    },
    methods: {
        selectLesson(lesson) {
            this.$emit("lessonSelected", lesson);
        },
        selectControlQuestions(module) {
            // Создаём объект "урока" для контрольных вопросов модуля
            const controlLesson = {
                id: module.id + "_control",  // индивидуальный ID для контрольных вопросов
                title: "Қорытынды сұрақтар",
                // Обычно нет теоретического материала, поэтому pages пустой
                pages: [],
                // Вопросы будут браться из модуля
                questions: module.questions,
                // Для поиска модуля при необходимости сохраняем его id
                module: module.id,
            };
            this.$emit("lessonSelected", controlLesson);
        },
    },
};
</script>

<style scoped>
/* Дополнительные стили, если необходимо */
</style>