<template>
    <div class="flex h-screen">
        <!-- Сол жақта орналасқан Sidebar -->
        <Sidebar :modules="modules" :currentLessonId="currentLesson.id" @lessonSelected="handleLessonSelected" />

        <!-- Негізгі аймақ: жоғарғы жағында сабақ бары және төменде сабақтың мазмұны -->
        <div class="flex-1 flex flex-col bg-white">
            <LessonProgressBar :totalSteps="computedTotalSteps" :currentStep="currentStep"
                @stepSelected="handleStepSelected" />
            <div class="p-6 overflow-auto flex-1">
                <LessonContent :lesson="currentLesson" :currentStep="currentStep" :totalSteps="computedTotalSteps"
                    @next="nextStep" />
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
            // Мысал ретінде модульдер мен сабақтардың құрылымы
            modules: [
                {
                    id: 1,
                    title: "1-модуль: Негіздер",
                    lessons: [
                        { id: 101, title: "1-сабақ: Ағылшын тілін таныстыру" },
                        { id: 102, title: "2-сабақ: Әліпби және негізгі тіркестер" },
                    ],
                },
                {
                    id: 2,
                    title: "2-модуль: Грамматика",
                    lessons: [
                        { id: 201, title: "3-сабақ: Сөз таптары" },
                        { id: 202, title: "4-сабақ: Ағылшын тіліндегі шақтар" },
                    ],
                },
            ],
            currentLesson: {
                id: 101,
                title: "1-сабақ: Ағылшын тілін таныстыру",
                pages: [
                    "Теория, 1-бет: Негізгі ұғымдар.",
                    "Теория, 2-бет: Қосымша ақпарат.",
                    "Теория, 3-бет: Бөлім қорытындылары.",
                ],
                questions: [
                    {
                        text: "«Hello» сөзі қазақша қалай аударылады?",
                        answers: ["Сәлем", "Сау бол", "Өтінемін", "Рақмет"],
                        correct: 0,
                    },
                    {
                        text: "Есептелетін зат есімнің біржақты түрінде қандай артикль қолданылады?",
                        answers: ["a/an", "the", "артикль жоқ", "екуі де"],
                        correct: 0,
                    },
                    // Қосымша сұрақтар қосуға болады...
                ],
            },
            currentStep: 1,
        };
    },
    computed: {
        computedTotalSteps() {
            // Барлық қадамдар: теория беттері мен сұрақтар саны
            return this.currentLesson.pages.length + this.currentLesson.questions.length;
        },
    },
    methods: {
        handleLessonSelected(lesson) {
            // Мысал ретінде жаңа сабақ объектісі
            this.currentLesson = {
                id: lesson.id,
                title: lesson.title,
                pages: [
                    "Теория, 1-бет: Негізгі ұғымдар және терминдер.",
                    "Теория, 2-бет: Негізгі грамматикалық құрылымдар.",
                    "Теория, 3-бет: Сөйлем құрылымы және сөз тіркестері.",
                    "Теория, 4-бет: Практикалық қолдану мысалдары.",
                    "Теория, 5-бет: Қорытынды, рефлексия және қосымша материалдар."
                ],
                questions: [
                    {
                        text: "Тест сұрағының мысалы 1: 'Hello' сөзінің қазақша аудармасы қандай?",
                        answers: ["Сәлем", "Сау бол", "Қош келдіңіз", "Рақмет"],
                        correct: 0
                    },
                    {
                        text: "Тест сұрағының мысалы 2: 'What is your name?' дегенді қазақша қалай аударамыз?",
                        answers: ["Сіздің атыңыз кім?", "Менің атым кім?", "Олардың аты кім?", "Біздің атымыз кім?"],
                        correct: 0
                    },
                    {
                        text: "Тест сұрағының мысалы 3: 'How are you?' деген сұрақтың дұрыс аудармасы қандай?",
                        answers: ["Қалайсың?", "Не істейсің?", "Қайырлы таң!", "Қайда барасың?"],
                        correct: 0
                    },
                    {
                        text: "Тест сұрағының мысалы 4: 'Thank you' сөзінің қазақша аудармасы қалай?",
                        answers: ["Рақмет", "Сәлем", "Кешіріңіз", "Сау бол"],
                        correct: 0
                    },
                    {
                        text: "Тест сұрағының мысалы 5: 'Goodbye' дегенді қазақша қалай аударамыз?",
                        answers: ["Сау бол", "Сәлем", "Қош келдіңіз", "Рақмет"],
                        correct: 0
                    }
                ]
            };
            this.currentStep = 1;
        },
        handleStepSelected(step) {
            this.currentStep = step;
        },
        nextStep() {
            // Отанды оқиға: жай ғана ағымдағы қадамды арттырады
            this.currentStep++;
        }
    }
};
</script>

<style scoped>
/* Қосымша стильдер қажет болса */
</style>