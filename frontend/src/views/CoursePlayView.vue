<template>
    <div class="flex h-screen">
        <!-- Сайдбар теперь больше и зафиксирован слева -->
        <Sidebar :modules="modules" :currentLessonId="currentLesson.id" @lessonSelected="handleLessonSelected" />

        <!-- Основная область -->
        <div class="flex-1 flex flex-col bg-white">
            <LessonProgressBar :totalSteps="totalSteps" :currentStep="currentStep" @stepSelected="handleStepSelected" />
            <div class="p-6 overflow-auto flex-1">
                <LessonContent :lesson="currentLesson" :currentStep="currentStep" />
            </div>
        </div>
    </div>
</template>

<script>
import Sidebar from "../components/Sidebar.vue";
import LessonProgressBar from "../components/LessonProgressBar.vue";
import LessonContent from "../components/LessonContent.vue";

export default {
    name: "CoursePlayView",
    components: {
        Sidebar,
        LessonProgressBar,
        LessonContent,
    },
    props: {
        courseId: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            // Примерная структура модулей и урока
            modules: [
                {
                    id: 1,
                    title: "Модуль 1: Основы",
                    lessons: [
                        { id: 101, title: "Урок 1: Введение в английский язык" },
                        { id: 102, title: "Урок 2: Алфавит и базовые фразы" },
                    ],
                },
                {
                    id: 2,
                    title: "Модуль 2: Грамматика",
                    lessons: [
                        { id: 201, title: "Урок 3: Части речи" },
                        { id: 202, title: "Урок 4: Времена в английском" },
                    ],
                },
            ],
            currentLesson: {
                id: 101,
                title: "Урок 1: Введение в английский язык",
                pages: [
                    "Теория, страница 1: Основные понятия.",
                    "Теория, страница 2: Дополнительная информация.",
                    "Теория, страница 3: Итоги раздела.",
                ],
                questions: [
                    {
                        text: "Как переводится слово 'Hello'?",
                        answers: ["Привет", "До свидания", "Пожалуйста", "Спасибо"],
                        correct: 0,
                    },
                    {
                        text: "Какой артикль употребляется с исчисляемыми существительными в единственном числе?",
                        answers: ["a/an", "the", "нет артикля", "и то, и другое"],
                        correct: 0,
                    },
                    // Остальные вопросы...
                ],
            },
            totalSteps: 13,
            currentStep: 1,
        };
    },
    methods: {
        handleLessonSelected(lesson) {
            this.currentLesson = {
                id: lesson.id,
                title: lesson.title,
                pages: [
                    "Теория, страница 1: Основные понятия.",
                    "Теория, страница 2: Дополнительная информация.",
                    "Теория, страница 3: Итоги раздела.",
                ],
                questions: [
                    {
                        text: "Пример тестового вопроса 1?",
                        answers: ["Ответ A", "Ответ B", "Ответ C", "Ответ D"],
                        correct: 0,
                    },
                    // Другие вопросы...
                ],
            };
            this.currentStep = 1;
        },
        handleStepSelected(step) {
            this.currentStep = step;
        },
    },
};
</script>

<style scoped>
/* Дополнительные стили, если необходимо */
</style>