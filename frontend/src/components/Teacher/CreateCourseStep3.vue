<template>
    <div class="max-w-4xl mx-auto">
        <h3 class="text-2xl font-bold text-blue-800 mb-4">Шаг 3: Уроки и вопросы</h3>
        <p class="mb-6 text-gray-700">
            Текущий курс: <strong>{{ formData.name }}</strong>
        </p>

        <!-- Список модулей -->
        <div v-if="localModules.length" class="space-y-8">
            <div v-for="(mod, modIndex) in localModules" :key="mod.id" class="bg-white p-6 rounded-lg shadow border">
                <div class="mb-4">
                    <h4 class="text-xl font-semibold text-gray-800">
                        Модуль: {{ mod.title }}
                    </h4>
                    <p class="text-sm text-gray-600">{{ mod.description }}</p>
                </div>

                <!-- Раздел уроков -->
                <div class="mb-6">
                    <h5 class="text-lg font-semibold text-gray-700 mb-3">
                        Уроки модуля
                    </h5>
                    <div v-if="mod.lessons.length">
                        <div v-for="(lesson, lessonIndex) in mod.lessons" :key="lessonIndex"
                            class="mb-4 p-4 border rounded bg-gray-50">
                            <p class="text-sm font-medium mb-2">
                                Урок #{{ lessonIndex + 1 }}
                            </p>
                            <label class="block text-gray-700 text-sm font-medium mb-1">
                                Название урока
                            </label>
                            <input v-model="lesson.title" type="text" placeholder="Напр. 'Lesson 1: Basics'"
                                class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition" />
                            <label class="block text-gray-700 text-sm font-medium mt-3 mb-1">
                                Содержание урока
                            </label>
                            <textarea v-model="lesson.content" placeholder="Текст урока..."
                                class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition"
                                rows="3"></textarea>
                        </div>
                    </div>
                    <button @click="addLesson(modIndex)"
                        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded transition text-sm">
                        Добавить урок
                    </button>
                </div>

                <!-- Раздел вопросов -->
                <div>
                    <h5 class="text-lg font-semibold text-gray-700 mb-3">
                        Вопросы модуля (итоговая аттестация)
                    </h5>
                    <div v-if="mod.questions.length">
                        <div v-for="(question, qIndex) in mod.questions" :key="qIndex"
                            class="mb-4 p-4 border rounded bg-gray-50">
                            <p class="text-sm font-medium mb-2">
                                Вопрос #{{ qIndex + 1 }}
                            </p>
                            <!-- Текст вопроса -->
                            <label class="block text-gray-700 text-sm font-medium mb-1">
                                Текст вопроса
                            </label>
                            <input v-model="question.question_text" type="text"
                                placeholder="Напр. 'What is the capital of France?'"
                                class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />

                            <!-- Выбор типа вопроса -->
                            <label class="block text-gray-700 text-sm font-medium mt-3 mb-1">
                                Тип вопроса
                            </label>
                            <select v-model="question.question_type"
                                class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm">
                                <option value="">-- Выберите тип --</option>
                                <option v-for="type in questionTypes" :key="type.id" :value="type.id">
                                    {{ type.name }}
                                </option>
                            </select>

                            <!-- Параметры вопроса -->
                            <div class="grid grid-cols-3 gap-4 mt-3">
                                <div>
                                    <label class="block text-gray-700 text-sm font-medium mb-1">
                                        Макс. балл
                                    </label>
                                    <input v-model.number="question.max_score" type="number" placeholder="5"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />
                                </div>
                                <div>
                                    <label class="block text-gray-700 text-sm font-medium mb-1">
                                        Лимит времени (сек)
                                    </label>
                                    <input v-model.number="question.time_limit" type="number" placeholder="60"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />
                                </div>
                                <div>
                                    <label class="block text-gray-700 text-sm font-medium mb-1">
                                        Макс. попыток
                                    </label>
                                    <input v-model.number="question.max_attempts" type="number" placeholder="3"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />
                                </div>
                            </div>

                            <!-- Поле для правильного ответа / вариантов ответа -->
                            <div class="mt-4">
                                <!-- Если тип text -->
                                <div v-if="question.question_type === questionTypeIds.text">
                                    <label class="block text-gray-700 text-sm font-medium mb-1">
                                        Правильный ответ
                                    </label>
                                    <input v-model="question.correct_answer" type="text" placeholder="Напр. 'Paris'"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />
                                </div>
                                <!-- Если тип boolean -->
                                <div v-else-if="question.question_type === questionTypeIds.boolean">
                                    <label class="block text-gray-700 text-sm font-medium mb-1">
                                        Правильный ответ
                                    </label>
                                    <select v-model="question.correct_answer"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm">
                                        <option value="">-- Выберите --</option>
                                        <option value="true">Да</option>
                                        <option value="false">Нет</option>
                                    </select>
                                </div>
                                <!-- Если тип file -->
                                <div v-else-if="question.question_type === questionTypeIds.file">
                                    <label class="block text-gray-700 text-sm font-medium mb-1">
                                        Комментарий к файлу
                                    </label>
                                    <input v-model="question.correct_answer" type="text" placeholder="(необязательно)"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />
                                    <!-- Здесь можно добавить кнопку для загрузки файла -->
                                </div>
                                <!-- Если тип quiz -->
                                <div v-else-if="question.question_type === questionTypeIds.quiz">
                                    <p class="text-gray-700 text-sm font-medium mb-2">
                                        Варианты ответов
                                    </p>
                                    <div v-for="(option, optIndex) in question.answer_options" :key="optIndex"
                                        class="flex items-center mb-2 space-x-3">
                                        <input v-model="option.answer_text" type="text" placeholder="Вариант ответа"
                                            class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />
                                        <label class="flex items-center space-x-1">
                                            <input type="checkbox" v-model="option.is_correct"
                                                class="form-checkbox text-blue-600" />
                                            <span class="text-sm text-gray-700">Правильный?</span>
                                        </label>
                                    </div>
                                    <button @click="addQuizOption(modIndex, qIndex)"
                                        class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm transition">
                                        Добавить вариант
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Кнопка для добавления нового вопроса -->
                    <button @click="addQuestion(modIndex)"
                        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded text-sm transition">
                        Добавить вопрос
                    </button>
                </div>
            </div>
        </div>

        <div v-else class="text-gray-600 mb-4">
            Нет модулей (или не загружены).
        </div>

        <!-- Кнопки управления шагами -->
        <div class="flex justify-between mt-8">
            <button @click="$emit('back')"
                class="bg-gray-500 hover:bg-gray-600 text-white px-5 py-3 rounded-lg transition">
                Назад
            </button>
            <button @click="emitFinish"
                class="bg-blue-500 hover:bg-blue-600 text-white px-5 py-3 rounded-lg transition">
                Завершить создание
            </button>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "CreateCourseStep3",
    props: {
        formData: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            localModules: [],
            questionTypes: [],
            questionTypeIds: {},
        };
    },
    created() {
        // Инициализируем модули из formData и дополняем их, если нужно
        this.localModules = this.formData.modules.map((m) => ({
            ...m,
            lessons: m.lessons || [],
            questions: m.questions || [],
        }));
        this.fetchQuestionTypes();
    },
    methods: {
        async fetchQuestionTypes() {
            try {
                const response = await axios.get("/api/question-types/");
                this.questionTypes = response.data;
                // Формируем объект соответствия, например: { text: "uuid1", quiz: "uuid2", ... }
                this.questionTypes.forEach((type) => {
                    this.questionTypeIds[type.name] = type.id;
                });
            } catch (error) {
                console.error("Ошибка получения типов вопросов:", error);
            }
        },
        addLesson(modIndex) {
            this.localModules[modIndex].lessons.push({
                title: "",
                content: "",
            });
        },
        addQuestion(modIndex) {
            this.localModules[modIndex].questions.push({
                question_text: "",
                question_type: "", // будет выбран из выпадающего списка (id)
                time_limit: 60,
                max_attempts: 3,
                max_score: 5,
                correct_answer: "",
                answer_options: [],
            });
        },
        addQuizOption(modIndex, qIndex) {
            const question = this.localModules[modIndex].questions[qIndex];
            if (!question.answer_options) {
                question.answer_options = [];
            }
            question.answer_options.push({
                answer_text: "",
                is_correct: false,
            });
        },
        emitFinish() {
            // Передаём все данные наверх, чтобы родитель сделал POST-запросы
            this.$emit("finish", { modules: this.localModules });
        },
    },
    watch: {
        localModules: {
            handler(newVal) {
                this.$emit("update", { modules: newVal });
            },
            deep: true,
        },
    },
};
</script>

<style scoped>
/* Дополнительные стили при необходимости */
</style>