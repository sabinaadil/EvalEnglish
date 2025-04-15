<template>
    <div class="max-w-4xl mx-auto">
        <h3 class="text-2xl font-bold text-blue-800 mb-4">Қадам 3: Сабақтар мен сұрақтар</h3>
        <p class="mb-6 text-gray-700">
            Ағымдағы курс: <strong>{{ formData.name }}</strong>
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
                        Модуль сабақтары
                    </h5>
                    <div v-if="mod.lessons.length">
                        <div v-for="(lesson, lessonIndex) in mod.lessons" :key="lessonIndex"
                            class="mb-4 p-4 border rounded bg-gray-50">
                            <p class="text-sm font-medium mb-2">
                                Сабақ #{{ lessonIndex + 1 }}
                            </p>
                            <label class="block text-gray-700 text-sm font-medium mb-1">
                                Сабақ атауы
                            </label>
                            <input v-model="lesson.title" type="text" placeholder="Мыс. 'Lesson 1: Basics'"
                                class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition" />

                            <label class="block text-gray-700 text-sm font-medium mt-3 mb-1">
                                Сабақ мазмұны
                            </label>
                            <div :id="'vditor-' + modIndex + '-' + lessonIndex" class="vditor-container"></div>
                        </div>
                    </div>
                    <button @click="addLesson(modIndex)"
                        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded transition text-sm">
                        Сабақты тіркеу
                    </button>
                </div>

                <!-- Раздел вопросов -->
                <div>
                    <h5 class="text-lg font-semibold text-gray-700 mb-3">
                        Модуль сұрақтары (Қорытынды тестілеу)
                    </h5>
                    <div v-if="mod.questions.length">
                        <div v-for="(question, qIndex) in mod.questions" :key="qIndex"
                            class="mb-4 p-4 border rounded bg-gray-50">
                            <p class="text-sm font-medium mb-2">
                                Сұрақ #{{ qIndex + 1 }}
                            </p>
                            <label class="block text-gray-700 text-sm font-medium mb-1">
                                Сұрақ мәтіні
                            </label>
                            <input v-model="question.question_text" type="text"
                                placeholder="Мыс. 'What is the capital of France?'"
                                class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />

                            <label class="block text-gray-700 text-sm font-medium mt-3 mb-1">
                                Сұрақ түрі
                            </label>
                            <select v-model="question.question_type"
                                class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm">
                                <option value="">Сұрақ түрін таңдаңыз</option>
                                <option v-for="type in questionTypes" :key="type.id" :value="type.id">
                                    {{ type.name }}
                                </option>
                            </select>

                            <div class="grid grid-cols-3 gap-4 mt-3">
                                <div>
                                    <label class="block text-gray-700 text-sm font-medium mb-1">
                                        Максималды ұпай
                                    </label>
                                    <input v-model.number="question.max_score" type="number" placeholder="5"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />
                                </div>
                                <div>
                                    <label class="block text-gray-700 text-sm font-medium mb-1">
                                        Уақыт шегі (сек)
                                    </label>
                                    <input v-model.number="question.time_limit" type="number" placeholder="60"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />
                                </div>
                                <div>
                                    <label class="block text-gray-700 text-sm font-medium mb-1">
                                        Максималды мүмкіндік
                                    </label>
                                    <input v-model.number="question.max_attempts" type="number" placeholder="3"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />
                                </div>
                            </div>

                            <div class="mt-4">
                                <div v-if="question.question_type === questionTypeIds.text">
                                    <label class="block text-gray-700 text-sm font-medium mb-1">
                                        Дұрыс жауап
                                    </label>
                                    <input v-model="question.correct_answer" type="text" placeholder="Мыс. 'Paris'"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />
                                </div>

                                <div v-else-if="question.question_type === questionTypeIds.boolean">
                                    <label class="block text-gray-700 text-sm font-medium mb-1">
                                        Дүрыс жауап
                                    </label>
                                    <select v-model="question.correct_answer"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm">
                                        <option value="">-- Выберите --</option>
                                        <option value="true">Иә</option>
                                        <option value="false">Жоқ</option>
                                    </select>
                                </div>

                                <div v-else-if="question.question_type === questionTypeIds.file">
                                    <label class="block text-gray-700 text-sm font-medium mb-1">
                                        Файл үшін сипаттама
                                    </label>
                                    <input v-model="question.correct_answer" type="text" placeholder="(необязательно)"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />
                                </div>

                                <div v-else-if="question.question_type === questionTypeIds.quiz">
                                    <p class="text-gray-700 text-sm font-medium mb-2">
                                        Жауаптар варианттары
                                    </p>
                                    <div v-for="(option, optIndex) in question.answer_options" :key="optIndex"
                                        class="flex items-center mb-2 space-x-3">
                                        <input v-model="option.answer_text" type="text"
                                            placeholder="Жауап вариантын еңгізіңіз..."
                                            class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500 transition text-sm" />
                                        <label class="flex items-center space-x-1">
                                            <input type="checkbox" v-model="option.is_correct"
                                                class="form-checkbox text-blue-600" />
                                            <span class="text-sm text-gray-700">Дұрыс?</span>
                                        </label>
                                    </div>
                                    <button @click="addQuizOption(modIndex, qIndex)"
                                        class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm transition">
                                        Вариант қосу
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button @click="addQuestion(modIndex)"
                        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded text-sm transition">
                        Сұрақ қосу
                    </button>
                </div>
            </div>
        </div>

        <div v-else class="text-gray-600 mb-4">
            Модульдер жоқ немесе жүктелмеген!
        </div>

        <!-- Кнопки управления шагами -->
        <div class="flex justify-between mt-8">
            <button @click="$emit('back')"
                class="bg-gray-500 hover:bg-gray-600 text-white px-5 py-3 rounded-lg transition">
                Артқа
            </button>
            <button @click="emitFinish"
                class="bg-blue-500 hover:bg-blue-600 text-white px-5 py-3 rounded-lg transition">
                Аяқтау
            </button>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import Vditor from 'vditor';
import 'vditor/dist/index.css';

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
            vditorInstances: {},
        };
    },
    created() {
        this.localModules = this.formData.modules.map((m) => ({
            ...m,
            lessons: m.lessons?.map(lesson => ({
                ...lesson,
                content: lesson.content || ""
            })) || [],
            questions: m.questions || [],
        }));
        this.fetchQuestionTypes();
    },
    mounted() {
        this.$nextTick(() => {
            this.initAllEditors();
        });
    },
    beforeUnmount() {
        this.destroyAllEditors();
    },
    methods: {
        initAllEditors() {
            this.localModules.forEach((mod, modIndex) => {
                mod.lessons.forEach((lesson, lessonIndex) => {
                    this.initVditor(modIndex, lessonIndex, lesson.content);
                });
            });
        },

        initVditor(modIndex, lessonIndex, initialContent) {
            const containerId = `vditor-${modIndex}-${lessonIndex}`;
            const instanceKey = `${modIndex}-${lessonIndex}`;

            if (this.vditorInstances[instanceKey]) return;

            this.vditorInstances[instanceKey] = new Vditor(containerId, {
                height: 300,
                value: initialContent,
                cache: {
                    enable: false
                },
                input: (value) => {
                    this.localModules[modIndex].lessons[lessonIndex].content = value;
                },
                upload: {
                    handler(files) {
                        return new Promise((resolve) => {
                            // Реализуйте загрузку файлов при необходимости
                            console.log('Files to upload:', files);
                            resolve(['/dummy/path/file.png']);
                        });
                    }
                },
                toolbar: [
                    'emoji', 'headings', 'bold', 'italic', 'link',
                    'upload', 'code', 'table', 'undo', 'redo'
                ]
            });
        },

        destroyEditor(modIndex, lessonIndex) {
            const key = `${modIndex}-${lessonIndex}`;
            if (this.vditorInstances[key]) {
                this.vditorInstances[key].destroy();
                delete this.vditorInstances[key];
            }
        },

        destroyAllEditors() {
            Object.keys(this.vditorInstances).forEach(key => {
                this.vditorInstances[key].destroy();
            });
            this.vditorInstances = {};
        },

        async fetchQuestionTypes() {
            try {
                const response = await axios.get("/api/question-types/");
                this.questionTypes = response.data;
                this.questionTypes.forEach((type) => {
                    this.questionTypeIds[type.name] = type.id;
                });
            } catch (error) {
                console.error("Ошибка получения типов вопросов:", error);
            }
        },

        addLesson(modIndex) {
            const newLesson = {
                title: "",
                content: "",
            };

            this.localModules[modIndex].lessons.push(newLesson);

            this.$nextTick(() => {
                const lessonIndex = this.localModules[modIndex].lessons.length - 1;
                this.initVditor(modIndex, lessonIndex, "");
            });
        },

        addQuestion(modIndex) {
            this.localModules[modIndex].questions.push({
                question_text: "",
                question_type: "",
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
            this.$emit("finish", { modules: this.localModules });
        },
    },
    watch: {
        localModules: {
            handler(newVal) {
                this.$emit("update", { modules: newVal });
                this.$nextTick(this.initAllEditors);
            },
            deep: true,
            immediate: true
        }
    }
};
</script>

<style scoped>
.vditor-container {
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 8px;
}

.vditor-toolbar {
    background-color: #f8fafc !important;
    border-bottom: 1px solid #e2e8f0 !important;
    padding: 4px !important;
}

.vditor-reset {
    padding: 12px !important;
    min-height: 200px;
    background-color: white;
}

.vditor-reset pre {
    background-color: #f3f4f6 !important;
    padding: 12px !important;
    border-radius: 4px;
}

.vditor-reset table {
    border-collapse: collapse;
}

.vditor-reset td,
.vditor-reset th {
    border: 1px solid #e5e7eb;
    padding: 6px 12px;
}
</style>