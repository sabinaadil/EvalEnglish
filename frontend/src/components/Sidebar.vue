<template>
    <div class="bg-gray-900 text-white w-80 flex-none p-4 overflow-auto rounded-lg">
        <div v-for="module in modules" :key="module.id" class="mb-6">
            <h3 class="text-lg font-semibold mb-2">
                {{ module.title }}
            </h3>
            <ul class="space-y-1">
                <li v-for="lesson in module.lessons" :key="lesson.id"
                    class="cursor-pointer px-2 py-1 rounded flex items-center" :class="{
                        'bg-gray-700': lesson.id === currentLessonId,
                        'hover:bg-gray-700': lesson.id !== currentLessonId
                    }" @click="selectLesson(lesson)">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                    {{ lesson.title }}
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
            type: Number,
            default: null,
        },
    },
    methods: {
        selectLesson(lesson) {
            this.$emit("lessonSelected", lesson);
        },
    },
};
</script>

<style scoped>
/* Қосымша стильдер */
</style>