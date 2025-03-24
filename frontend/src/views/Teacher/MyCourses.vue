<template>
    <div class="container mx-auto p-6">
        <!-- Если мастер НЕ запущен, показываем список курсов в виде карточек -->
        <div v-if="!wizardActive">
            <h1 class="text-3xl font-bold mb-6">Менің курстарым</h1>
            <button @click="startWizard"
                class="bg-green-500 text-white px-5 py-2 rounded-lg shadow mb-8 hover:bg-green-600 transition">
                Жаңа курс ашу
            </button>

            <div>
                <h2 class="text-xl font-semibold mb-4">Сіздің ағымдағы курстар тізімі</h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    <CourseCard v-for="course in courses" :key="course.id" :course="course" :showOptions="true" />
                </div>
            </div>
        </div>

        <!-- Если мастер запущен, показываем пошаговую форму -->
        <div v-else class="mb-6 border rounded-lg p-6 shadow-lg bg-white">
            <div class="mb-4">
                <h2 class="text-2xl font-semibold">Шаг {{ currentStep }} из 3</h2>
            </div>
            <component :is="currentStepComponent" :form-data="formData" @update="updateFormData" @next="handleNext"
                @back="handleBack" @finish="finishWizard" />
        </div>
    </div>
</template>

<script>
import axios from "axios";
import CreateCourseStep1 from "../../components/Teacher/CreateCourseStep1.vue";
import CreateCourseStep2 from "../../components/Teacher/CreateCourseStep2.vue";
import CreateCourseStep3 from "../../components/Teacher/CreateCourseStep3.vue";
import CourseCard from "../../components/CourseCard.vue";

export default {
    name: "TeacherMyCourses",
    components: {
        CreateCourseStep1,
        CreateCourseStep2,
        CreateCourseStep3,
        CourseCard,
    },
    data() {
        return {
            wizardActive: false,
            currentStep: 1,
            formData: {
                // Шаг 1 – данные курса
                name: "",
                description: "",
                courseId: null, // ID курса, вернётся с бэка
                // Шаг 2 – модули курса (массив объектов)
                modules: [],
                // На шаге 3 модули будут содержать уроки и вопросы
            },
            courses: [], // Список курсов преподавателя
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
    },
    methods: {
        startWizard() {
            this.wizardActive = true;
            this.currentStep = 1;
            // Сброс formData
            this.formData = {
                name: "",
                description: "",
                courseId: null,
                modules: [],
            };
        },
        updateFormData(updatedData) {
            // Объединяем данные, полученные от дочерних компонентов, с formData
            this.formData = { ...this.formData, ...updatedData };
        },

        /**
         * Обработка кнопки "Далее" (Шаг 1 -> 2 или Шаг 2 -> 3)
         */
        async handleNext(updatedData) {
            this.updateFormData(updatedData);

            // === Шаг 1: Создание курса ===
            if (this.currentStep === 1) {
                try {
                    const response = await axios.post("/api/course/", {
                        name: this.formData.name,
                        description: this.formData.description,
                    });
                    // Предполагаем, что сервер возвращает объект вида: { course: { id, name, ... } }
                    this.formData.courseId = response.data.course.id;
                    this.formData.name = response.data.course.name; // обновляем название курса
                    console.log("Курс создан:", response.data);
                } catch (error) {
                    console.error("Ошибка создания курса:", error);
                    return;
                }
            }
            // === Шаг 2: Создание модулей ===
            else if (this.currentStep === 2) {
                try {
                    for (let i = 0; i < this.formData.modules.length; i++) {
                        const moduleData = this.formData.modules[i];
                        if (!moduleData.title) {
                            console.error(`Модуль ${i + 1} не имеет названия`);
                            continue;
                        }
                        const modResponse = await axios.post("/api/module/", {
                            course: this.formData.courseId,
                            title: moduleData.title,
                            description: moduleData.description,
                            order: moduleData.order,
                            due_date: moduleData.due_date || null,
                        });
                        // Сохраняем реальный id модуля, полученный с сервера
                        this.formData.modules[i].id = modResponse.data.module.id;
                    }
                    console.log("Модули сохранены");
                } catch (error) {
                    console.error("Ошибка создания модуля:", error);
                    return;
                }
            }

            // Если не последний шаг, переходим к следующему
            if (this.currentStep < 3) {
                this.currentStep++;
            }
        },

        /**
         * Обработка кнопки "Назад"
         */
        handleBack() {
            if (this.currentStep > 1) {
                this.currentStep--;
            } else {
                this.wizardActive = false;
            }
        },

        /**
         * Завершение мастера (Шаг 3): создание уроков и вопросов (включая варианты ответа)
         */
        async finishWizard(updatedData) {
            this.updateFormData(updatedData);

            try {
                // Перебираем модули
                for (const mod of this.formData.modules) {
                    // 1) Уроки
                    if (mod.lessons && mod.lessons.length) {
                        for (const lesson of mod.lessons) {
                            if (!lesson.title) {
                                console.error("Урок для модуля", mod.title, "не имеет названия");
                                continue;
                            }
                            const lessonResp = await axios.post("/api/lesson/", {
                                module: mod.id,
                                title: lesson.title,
                                description: lesson.description,
                                order: lesson.order || 1,
                                content: lesson.content,
                            });
                            console.log("Урок создан:", lessonResp.data);
                        }
                    }

                    // 2) Вопросы
                    if (mod.questions && mod.questions.length) {
                        for (const question of mod.questions) {
                            if (!question.question_text) {
                                console.error("Вопрос для модуля", mod.title, "не имеет текста");
                                continue;
                            }
                            // Создаём вопрос
                            const questionResp = await axios.post("/api/question/", {
                                module: mod.id,
                                question_text: question.question_text,
                                question_type: question.question_type,
                                time_limit: question.time_limit,
                                max_attempts: question.max_attempts,
                                max_score: question.max_score,
                                correct_answer: question.correct_answer,
                            });
                            console.log("Вопрос создан:", questionResp.data);

                            // Если у вопроса есть варианты (quiz), отправляем /api/answer-option/
                            if (question.answer_options && question.answer_options.length > 0) {
                                const questionId = questionResp.data?.question?.id || questionResp.data?.id;
                                if (!questionId) {
                                    console.warn("Не удалось получить ID вопроса из ответа:", questionResp.data);
                                    continue;
                                }
                                for (const option of question.answer_options) {
                                    await axios.post("/api/answer-option/", {
                                        question: questionId,
                                        answer_text: option.answer_text,
                                        is_correct: option.is_correct,
                                    });
                                }
                                console.log("Варианты ответа для quiz сохранены");
                            }
                        }
                    }
                }

                console.log("Уроки и вопросы сохранены");
            } catch (error) {
                console.error("Ошибка создания урока или вопроса:", error);
                return;
            }

            // Завершаем мастер: сбрасываем шаг и обновляем список курсов
            this.wizardActive = false;
            this.currentStep = 1;
            this.fetchCourses();
        },

        /**
         * Загрузка списка курсов
         */
        async fetchCourses() {
            try {
                const response = await axios.get("/api/courses-list/");
                // Извлекаем массив курсов из поля results
                this.courses = response.data.results;
            } catch (error) {
                console.error("Ошибка получения курсов:", error);
            }
        },
    },

    mounted() {
        this.fetchCourses();
    },
};
</script>

<style scoped>
/* Дополнительная стилизация для плавных переходов и отступов */
</style>