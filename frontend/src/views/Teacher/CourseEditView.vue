<template>
    <div class="container mx-auto p-6">
        <h1 class="text-3xl font-bold mb-6">Курсты өңдеу</h1>
        <div v-if="loading" class="text-center text-gray-600">
            Курсты жүктеу...
        </div>
        <div v-else class="mb-6 border rounded-lg p-6 shadow-lg bg-white">
            <div class="mb-4">
                <h2 class="text-2xl font-semibold">3 тен {{ currentStep }}-ші Қадам</h2>
            </div>
            <component :is="currentStepComponent" :form-data="formData" @update="updateFormData" @next="handleNext"
                @back="handleBack" @finish="finishEditing" />
        </div>
    </div>
</template>

<script>
import axios from "axios";
import CreateCourseStep1 from "../../components/Teacher/CreateCourseStep1.vue";
import CreateCourseStep2 from "../../components/Teacher/CreateCourseStep2.vue";
import CreateCourseStep3 from "../../components/Teacher/CreateCourseStep3.vue";

export default {
    name: "CourseEditView",
    components: {
        CreateCourseStep1,
        CreateCourseStep2,
        CreateCourseStep3,
    },
    props: {
        id: {
            type: String,
            default: null,  // если не передается как пропс, будем пытаться получить из $route.params
        },
    },
    data() {
        return {
            loading: true,
            currentStep: 1,
            formData: {
                name: "",
                description: "",
                courseId: null,
                modules: [],
            },
        };
    },
    computed: {
        currentStepComponent() {
            switch (this.currentStep) {
                case 1:
                    return "CreateCourseStep1";
                case 2:
                    return "CreateCourseStep2";
                case 3:
                    return "CreateCourseStep3";
                default:
                    return "div";
            }
        },
        courseId() {
            // Попытка взять значение из пропса или параметров маршрута
            const id = this.id || (this.$route && this.$route.params && this.$route.params.id);
            console.log("Computed courseId:", id);
            return id;
        },
    },
    methods: {
        async fetchCourseData() {
            const cid = this.courseId;
            if (!cid) {
                console.error("Course ID is undefined");
                this.loading = false;
                return;
            }
            try {
                const response = await axios.get(`/api/course/${cid}/`);
                console.log("Response from API in fetchCourseData:", response.data);
                const courseData = response.data.course || response.data;
                const modulesData = response.data.modules || courseData.modules || [];
                this.formData.courseId = courseData.id;
                this.formData.name = courseData.name;
                this.formData.description = courseData.description;
                this.formData.modules = modulesData.map((mod) => ({
                    ...mod,
                    lessons: mod.lessons || [],
                    questions: mod.questions || [],
                }));
                this.loading = false;
            } catch (error) {
                console.error("Ошибка загрузки данных курса:", error);
                this.loading = false;
            }
        },
        updateFormData(updatedData) {
            this.formData = { ...this.formData, ...updatedData };
        },
        async handleNext(updatedData) {
            this.updateFormData(updatedData);
            if (this.currentStep === 1) {
                try {
                    const response = await axios.put(`/api/course/${this.courseId}/`, {
                        name: this.formData.name,
                        description: this.formData.description,
                    });
                    console.log("Курс обновлен:", response.data);
                } catch (error) {
                    console.error("Ошибка обновления курса:", error);
                    return;
                }
            } else if (this.currentStep === 2) {
                try {
                    for (let i = 0; i < this.formData.modules.length; i++) {
                        const moduleData = this.formData.modules[i];
                        if (!moduleData.title) {
                            console.error(`Модуль ${i + 1} не имеет названия`);
                            continue;
                        }
                        if (moduleData.id) {
                            await axios.put(`/api/module/${moduleData.id}/`, {
                                title: moduleData.title,
                                description: moduleData.description,
                                order: moduleData.order,
                                due_date: moduleData.due_date || null,
                            });
                        } else {
                            const modResponse = await axios.post("/api/module/", {
                                course: this.formData.courseId,
                                title: moduleData.title,
                                description: moduleData.description,
                                order: moduleData.order,
                                due_date: moduleData.due_date || null,
                            });
                            this.formData.modules[i].id = modResponse.data.module.id;
                        }
                    }
                    console.log("Модули обновлены");
                } catch (error) {
                    console.error("Ошибка обновления модулей:", error);
                    return;
                }
            }
            if (this.currentStep < 3) {
                this.currentStep++;
            }
        },
        handleBack() {
            if (this.currentStep > 1) {
                this.currentStep--;
            } else {
                this.$router.push({ name: "teacher-my-courses" });
            }
        },
        async finishEditing(updatedData) {
            this.updateFormData(updatedData);
            try {
                for (const mod of this.formData.modules) {
                    if (mod.lessons && mod.lessons.length) {
                        for (const lesson of mod.lessons) {
                            if (!lesson.title) {
                                console.error("Урок для модуля", mod.title, "не имеет названия");
                                continue;
                            }
                            if (lesson.id) {
                                await axios.put(`/api/lesson/${lesson.id}/`, {
                                    title: lesson.title,
                                    description: lesson.description,
                                    order: lesson.order || 1,
                                    content: lesson.content,
                                });
                            } else {
                                await axios.post("/api/lesson/", {
                                    module: mod.id,
                                    title: lesson.title,
                                    description: lesson.description,
                                    order: lesson.order || 1,
                                    content: lesson.content,
                                });
                            }
                        }
                    }
                    if (mod.questions && mod.questions.length) {
                        for (const question of mod.questions) {
                            if (!question.question_text) {
                                console.error("Вопрос для модуля", mod.title, "не имеет текста");
                                continue;
                            }
                            let questionResp;
                            if (question.id) {
                                questionResp = await axios.put(`/api/question/${question.id}/`, {
                                    question_text: question.question_text,
                                    question_type: question.question_type,
                                    time_limit: question.time_limit,
                                    max_attempts: question.max_attempts,
                                    max_score: question.max_score,
                                    correct_answer: question.correct_answer,
                                });
                            } else {
                                questionResp = await axios.post("/api/question/", {
                                    module: mod.id,
                                    question_text: question.question_text,
                                    question_type: question.question_type,
                                    time_limit: question.time_limit,
                                    max_attempts: question.max_attempts,
                                    max_score: question.max_score,
                                    correct_answer: question.correct_answer,
                                });
                            }
                            console.log("Вопрос сохранен:", questionResp.data);
                            if (question.answer_options && question.answer_options.length > 0) {
                                const questionId = questionResp.data?.question?.id || questionResp.data?.id;
                                if (!questionId) {
                                    console.warn("Не удалось получить ID вопроса:", questionResp.data);
                                    continue;
                                }
                                for (const option of question.answer_options) {
                                    if (option.id) {
                                        await axios.put(`/api/answer-option/${option.id}/`, {
                                            answer_text: option.answer_text,
                                            is_correct: option.is_correct,
                                        });
                                    } else {
                                        await axios.post("/api/answer-option/", {
                                            question: questionId,
                                            answer_text: option.answer_text,
                                            is_correct: option.is_correct,
                                        });
                                    }
                                }
                                console.log("Варианты ответа для quiz сохранены");
                            }
                        }
                    }
                }
                console.log("Курс обновлен");
            } catch (error) {
                console.error("Ошибка обновления урока или вопроса:", error);
                return;
            }
            this.$router.push({ name: "teacher-my-courses" });
        },
    },
    mounted() {
        this.fetchCourseData();
    },
};
</script>

<style scoped>
/* Дополнительные стили можно добавить по необходимости */
</style>