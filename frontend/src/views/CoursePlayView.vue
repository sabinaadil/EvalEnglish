<template>
    <div class="flex h-screen">
        <Sidebar :modules="modules" :currentLessonId="currentLesson ? currentLesson.id : null"
            @lessonSelected="handleLessonSelected" />
        <div class="flex-1 flex flex-col bg-white">
            <div v-if="currentLesson">
                <LessonProgressBar :totalSteps="computedTotalSteps" :currentStep="currentStep"
                    @stepSelected="handleStepSelected" />
                <div class="p-6 overflow-auto flex-1">
                    <LessonContent :lesson="currentLesson" :currentStep="currentStep" :totalSteps="computedTotalSteps"
                        @nextModule="handleNextModule" @nextLesson="handleNextLesson" @next="nextStep" />
                </div>
            </div>
            <div v-else class="flex-1 flex items-center justify-center">
                <p class="text-gray-500">Урок не выбран. Пожалуйста, выберите урок из списка.</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
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
            modules: [],
            currentLesson: null,
            currentStep: 1,
            loading: false,
            error: null,
        };
    },
    computed: {
        computedTotalSteps() {
            if (this.currentLesson) {
                if (this.currentLesson.content && this.currentLesson.content.trim().length > 0) {
                    return 1; // для теории
                } else if (Array.isArray(this.currentLesson.questions)) {
                    return this.currentLesson.questions.length;
                }
            }
            return 0;
        },
    },
    created() {
        this.fetchCoursePlayData();
    },
    methods: {
        async fetchCoursePlayData() {
            this.loading = true;
            try {
                const response = await axios.get(`/api/course-detail/${this.courseId}/`);
                const courseData = response.data;
                this.modules = courseData.modules || [];
                if (this.modules.length > 0) {
                    const firstModule = this.modules[0];
                    if (firstModule.lessons && firstModule.lessons.length > 0) {
                        const defaultLesson = firstModule.lessons[0];
                        if ((!defaultLesson.questions || defaultLesson.questions.length === 0) && firstModule.questions) {
                            defaultLesson.questions = firstModule.questions;
                        }
                        this.currentLesson = defaultLesson;
                    } else if (firstModule.questions && firstModule.questions.length > 0) {
                        this.currentLesson = {
                            id: firstModule.id + "_control",
                            title: "Контрольные сұрақтар",
                            content: "",
                            questions: firstModule.questions,
                            module: firstModule.id,
                        };
                    }
                    this.currentStep = 1;
                }
            } catch (err) {
                this.error = "Ошибка загрузки данных курса. Попробуйте позже.";
                console.error("Ошибка получения данных для прохождения курса:", err);
            } finally {
                this.loading = false;
            }
        },
        handleLessonSelected(lesson) {
            if ((!lesson.questions || lesson.questions.length === 0) && lesson.module) {
                const mod = this.modules.find(m => m.id === lesson.module);
                if (mod && mod.questions) {
                    lesson.questions = mod.questions;
                }
            }
            this.currentLesson = lesson;
            this.currentStep = 1;
        },
        handleStepSelected(step) {
            this.currentStep = step;
        },
        nextStep() {
            this.currentStep++;
        },
        handleNextModule() {
            const currentModuleId = this.currentLesson.module;
            const currentModuleIndex = this.modules.findIndex(m => m.id === currentModuleId);
            if (currentModuleIndex === -1) return;
            if (currentModuleIndex + 1 < this.modules.length) {
                const nextModule = this.modules[currentModuleIndex + 1];
                if (nextModule.lessons && nextModule.lessons.length > 0) {
                    let nextLesson = nextModule.lessons[0];
                    if ((!nextLesson.questions || nextLesson.questions.length === 0) && nextModule.questions) {
                        nextLesson.questions = nextModule.questions;
                    }
                    this.currentLesson = nextLesson;
                } else if (nextModule.questions && nextModule.questions.length > 0) {
                    this.currentLesson = {
                        id: nextModule.id + "_control",
                        title: "Контрольные сұрақтар",
                        content: "",
                        questions: nextModule.questions,
                        module: nextModule.id,
                    };
                }
                this.currentStep = 1;
            } else {
                alert("Вы успешно прошли курс!");
                // Можно также сделать редирект: this.$router.push('/course-completion')
            }
        },
        handleNextLesson() {
            // Переход к следующему уроку в текущем модуле
            const mod = this.modules.find(m => m.id === this.currentLesson.module);
            if (!mod || !mod.lessons) return;
            const currentIndex = mod.lessons.findIndex(l => l.id === this.currentLesson.id);
            if (currentIndex === -1) return;
            if (currentIndex + 1 < mod.lessons.length) {
                const nextLesson = mod.lessons[currentIndex + 1];
                if ((!nextLesson.questions || nextLesson.questions.length === 0) && mod.questions) {
                    nextLesson.questions = mod.questions;
                }
                this.currentLesson = nextLesson;
                this.currentStep = 1;
            } else {
                // Если уроков больше нет, переходим к контрольным вопросам, если они есть, иначе к следующему модулю
                if (mod.questions && mod.questions.length > 0) {
                    this.currentLesson = {
                        id: mod.id + "_control",
                        title: "Контрольные сұрақтар",
                        content: "",
                        questions: mod.questions,
                        module: mod.id,
                    };
                    this.currentStep = 1;
                } else {
                    // Если в модуле нет контрольных вопросов, автоматически переходим к следующему модулю
                    this.handleNextModule();
                }
            }
        },
    },
};
</script>

<style scoped>
/* Дополнительные стили, если необходимо */
</style>