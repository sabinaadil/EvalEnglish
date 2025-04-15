<template>
    <div class="max-w-3xl mx-auto px-6 py-8">
        <!-- Заголовок урока/вопроса -->
        <h2 class="text-3xl font-bold text-blue-800 mb-6 text-center">
            {{ lesson.title }}
        </h2>

        <!-- Если урок содержит теоретический контент -->
        <div v-if="hasContent" class="bg-gray-50 p-6 rounded-lg shadow">
            <div class="markdown-content" v-html="compiledMarkdown"></div>

            <!-- Кнопка "Следующий урок" для теоретических уроков -->
            <div class="flex justify-end mt-4">
                <button @click="emitNextLesson"
                    class="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg transition">
                    Келесі сабақ
                </button>
            </div>
        </div>

        <!-- Если это контрольный урок (с вопросами) -->
        <div v-else-if="hasQuestions" class="bg-gray-50 p-6 rounded-lg shadow">
            <h3 class="text-xl font-semibold mb-4">Қорытынды сұрақтар</h3>
            <p class="text-blue-700 font-medium mb-4">
                Сұрақ {{ currentQuestionIndex + 1 }} из {{ questionsCount }}
            </p>

            <!-- Текст вопроса с поддержкой Markdown -->
            <div class="text-gray-800 mb-4 font-medium markdown-content" v-if="currentQuestion"
                v-html="compiledQuestionText"></div>

            <!-- Информация: таймер и оставшиеся попытки -->
            <div class="flex justify-between items-center mb-4">
                <span class="text-sm text-gray-600">
                    Уақыт: <strong>{{ timeLeft }} сек.</strong>
                </span>
                <span class="text-sm text-gray-600">
                    Мүмкіндік қалды: <strong>{{ attemptsLeft }}</strong>
                </span>
            </div>

            <!-- Блок ввода ответа -->
            <div v-if="effectiveQuestionType === 'text'" class="mb-4">
                <textarea v-model="selectedAnswer" placeholder="Введите ваш ответ..."
                    class="w-full border border-gray-300 p-3 rounded focus:outline-none focus:border-blue-500 transition"></textarea>
            </div>

            <div v-else-if="currentQuestion.answer_options && currentQuestion.answer_options.length" class="space-y-3">
                <label v-for="(option, index) in currentQuestion.answer_options" :key="option.id"
                    class="flex items-center space-x-3">
                    <input type="radio" :name="'question-' + currentQuestion.id" :value="option.answer_text"
                        v-model="selectedAnswer" :disabled="inputsDisabled" class="form-radio text-green-500" />
                    <span class="text-gray-800">{{ option.answer_text }}</span>
                </label>
            </div>

            <!-- Блок кнопок -->
            <div class="flex justify-end mt-4 space-x-4 items-center">
                <div v-if="submissionMessage"
                    :class="{ 'text-green-600': isCorrectAnswer, 'text-red-600': !isCorrectAnswer }"
                    class="font-semibold">
                    {{ submissionMessage }}
                </div>

                <button v-if="!isCorrectAnswer && attemptsLeft > 0" @click="submitAnswer"
                    :disabled="inputsDisabled || timeLeft <= 0"
                    class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded transition disabled:opacity-50">
                    Жауап беру
                </button>

                <button v-else-if="isCorrectAnswer" @click="goNextModule"
                    class="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded transition">
                    Келесі модуль
                </button>
            </div>
        </div>

        <!-- Если ни контента, ни вопросов нет -->
        <div v-else class="text-gray-500">
            Контент немесе сұрақтар жоқ.
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { marked } from 'marked';
import DOMPurify from 'dompurify';

export default {
    name: "LessonContent",
    props: {
        lesson: {
            type: Object,
            required: true,
        },
        currentStep: {
            type: Number,
            default: 1,
        },
    },
    data() {
        return {
            selectedAnswer: "",
            submissionMessage: "",
            isCorrectAnswer: false,
            inputsDisabled: false,
            attemptNumber: 0,
            timer: null,
            timeLeft: 0,
        };
    },
    computed: {
        hasContent() {
            return this.lesson.content && this.lesson.content.trim().length > 0;
        },
        hasQuestions() {
            return Array.isArray(this.lesson.questions) && this.lesson.questions.length > 0;
        },
        questionsCount() {
            return this.hasQuestions ? this.lesson.questions.length : 0;
        },
        currentQuestionIndex() {
            return this.currentStep - 1;
        },
        currentQuestion() {
            if (this.hasQuestions) {
                return this.lesson.questions[this.currentQuestionIndex] || {};
            }
            return {};
        },
        attemptsLeft() {
            const max = this.currentQuestion.max_attempts || 1;
            const left = max - this.attemptNumber;
            return left < 0 ? 0 : left;
        },
        progress() {
            return this.questionsCount ? Math.round((this.currentStep / this.questionsCount) * 100) : 0;
        },
        effectiveQuestionType() {
            if (
                this.currentQuestion &&
                this.currentQuestion.correct_answer &&
                this.currentQuestion.correct_answer.trim().length > 0
            ) {
                return "text";
            }
            return this.currentQuestion && this.currentQuestion.question_type
                ? this.currentQuestion.question_type.toLowerCase()
                : "";
        },
        compiledMarkdown() {
            if (!this.hasContent) return '';
            return DOMPurify.sanitize(marked.parse(this.lesson.content));
        },
        compiledQuestionText() {
            if (!this.currentQuestion?.question_text) return '';
            return DOMPurify.sanitize(marked.parse(this.currentQuestion.question_text));
        },
    },
    watch: {
        lesson: {
            handler() {
                this.initQuestion();
            },
            immediate: true,
            deep: true,
        },
        currentQuestion: {
            handler(newVal) {
                this.initQuestion();
            },
            immediate: true,
            deep: true,
        },
    },
    methods: {
        initQuestion() {
            this.selectedAnswer = "";
            this.submissionMessage = "";
            this.isCorrectAnswer = false;
            this.inputsDisabled = false;
            this.attemptNumber = 0;
            this.clearTimer();
            if (this.currentQuestion && this.currentQuestion.time_limit) {
                this.timeLeft = this.currentQuestion.time_limit;
                this.startTimer();
            } else {
                this.timeLeft = 0;
            }
            if (this.currentQuestion.id) {
                this.fetchUserAnswers();
            }
        },
        startTimer() {
            this.clearTimer();
            if (this.timeLeft > 0) {
                this.timer = setInterval(() => {
                    if (this.timeLeft > 0) {
                        this.timeLeft--;
                    } else {
                        this.clearTimer();
                        if (!this.isCorrectAnswer) {
                            this.submissionMessage = "Уақыт өтті. Теорияны қайталаңыз және қайталап көріңіз.";
                            this.inputsDisabled = true;
                        }
                    }
                }, 1000);
            }
        },
        clearTimer() {
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
        },
        async fetchUserAnswers() {
            try {
                const resp = await axios.get(`/api/question/${this.currentQuestion.id}/my-answers/`);
                let userAnswers = resp.data || [];

                if (userAnswers.length === 0) return;

                userAnswers.sort((a, b) => new Date(a.submitted_at) - new Date(b.submitted_at));
                let bestAnswer = userAnswers.reduce((best, current) => {
                    const currentScore = parseFloat(current.model_score) || 0;
                    const bestScore = best ? (parseFloat(best.model_score) || 0) : -1;
                    return currentScore > bestScore ? current : best;
                }, null);

                this.attemptNumber = userAnswers.length;
                const modelScore = bestAnswer ? parseFloat(bestAnswer.model_score) || 0 : 0;
                const max = this.currentQuestion.max_attempts || 1;

                if (this.effectiveQuestionType === "text") {
                    if (modelScore >= 0.90) {
                        this.submissionMessage = "Өте дұрыс. Сіздің жауабыңыз оқытушыға тексеруге жіберілді.";
                        this.isCorrectAnswer = true;
                    } else if (modelScore >= 0.70) {
                        this.submissionMessage = "Керемет жауап бердіңіз. Сіздің жауабыңыз оқытушыға тексеруге жіберілді.";
                    } else if (modelScore >= 0.40) {
                        this.submissionMessage = "Жақсы жауап бердіңіз. Сіздің жауабыңыз оқытушыға тексеруге жіберілді.";
                    } else {
                        this.submissionMessage = "Нашар жауап бердіңіз. Сіздің жауабыңыз оқытушыға тексеруге жіберілді.";
                    }

                    if (!this.isCorrectAnswer && this.attemptNumber >= max) {
                        this.submissionMessage = "Сіз бұл сұрақтың барлық мүмкіндіктерін аяқтадыңыз.";
                        this.inputsDisabled = true;
                    } else if (this.isCorrectAnswer) {
                        this.inputsDisabled = true;
                    }
                    this.clearTimer();
                } else {
                    if (userAnswers.some(a => a.is_correct)) {
                        this.isCorrectAnswer = true;
                        this.submissionMessage = "Сіз бұл сұраққа дұрыс жауап бердіңіз.";
                        this.inputsDisabled = true;
                        this.clearTimer();
                    } else {
                        if (this.attemptNumber >= max) {
                            this.submissionMessage = "Сіз бұл сұрақтың барлық мүмкіндіктерін аяқтадыңыз.";
                            this.inputsDisabled = true;
                            this.clearTimer();
                        }
                    }
                }
            } catch (err) {
                console.error("Пайдаланушы жауаптарын алу қатесі:", err);
            }
        },
        async submitAnswer() {
            if (!this.selectedAnswer) {
                alert("Жауабыңызды енгізіңіз.");
                return;
            }
            try {
                this.attemptNumber++;
                const payload = {
                    question: this.currentQuestion.id,
                    answer_text: this.selectedAnswer,
                    time_spent: this.currentQuestion.time_limit ? (this.currentQuestion.time_limit - this.timeLeft) : 0,
                };
                const response = await axios.post("/api/answer/", payload);
                const answerData = response.data.answer;

                if (this.effectiveQuestionType === "text") {
                    const modelScore = parseFloat(answerData.model_score) || 0;
                    if (modelScore < 0.40) {
                        this.submissionMessage = `Нашар жауап берді. Мүмкіндік қалды: ${this.attemptsLeft}`;
                    } else if (modelScore < 0.70) {
                        this.submissionMessage = `Жақсы жауап берді. Мүмкіндік қалды: ${this.attemptsLeft}`;
                    } else if (modelScore < 0.90) {
                        this.submissionMessage = `Керемет жауап берді. Мүмкіндік қалды: ${this.attemptsLeft}`;
                    } else {
                        this.submissionMessage = "Өте дұрыс!";
                        this.isCorrectAnswer = true;
                    }
                    this.inputsDisabled = true;
                    this.clearTimer();
                } else {
                    this.isCorrectAnswer = !!answerData.is_correct;
                    const maxAttempts = this.currentQuestion.max_attempts || 1;
                    if (this.isCorrectAnswer) {
                        this.submissionMessage = "Сіз дұрыс жауап бердіңіз!";
                        this.inputsDisabled = true;
                        this.clearTimer();
                    } else {
                        if (this.attemptNumber < maxAttempts) {
                            this.submissionMessage = `Дұрыс емес. Мүмкіндік қалды: ${this.attemptsLeft}`;
                        } else {
                            this.submissionMessage = "Мүмкіндіктер таусылды!";
                            this.inputsDisabled = true;
                            this.clearTimer();
                        }
                    }
                }
            } catch (error) {
                console.error("Ошибка при отправке ответа:", error);
                alert("Ошибка при отправке ответа. Попробуйте позже.");
            }
        },
        goNextModule() {
            this.$emit("nextModule");
        },
        emitNextLesson() {
            this.$emit("nextLesson");
        },
    },
    beforeUnmount() {
        this.clearTimer();
    },
};
</script>

<style scoped>
.markdown-content {
    line-height: 1.6;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3 {
    margin: 1.5em 0 1em;
    color: #1a365d;
}

.markdown-content h1 {
    font-size: 2em;
    border-bottom: 2px solid #e2e8f0;
}

.markdown-content h2 {
    font-size: 1.5em;
}

.markdown-content h3 {
    font-size: 1.25em;
}

.markdown-content p {
    margin: 1em 0;
}

.markdown-content ul,
.markdown-content ol {
    padding-left: 2em;
    margin: 1em 0;
}

.markdown-content li {
    margin: 0.5em 0;
}

.markdown-content code {
    background-color: #f3f4f6;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: monospace;
}

.markdown-content pre {
    background-color: #f3f4f6;
    padding: 1em;
    border-radius: 6px;
    overflow-x: auto;
    margin: 1em 0;
}

.markdown-content pre code {
    background-color: transparent;
    padding: 0;
}

.markdown-content blockquote {
    border-left: 4px solid #cbd5e0;
    padding-left: 1em;
    color: #4a5568;
    margin: 1em 0;
}

.markdown-content table {
    border-collapse: collapse;
    margin: 1em 0;
    width: 100%;
}

.markdown-content th,
.markdown-content td {
    border: 1px solid #cbd5e0;
    padding: 0.75em;
    text-align: left;
}

.markdown-content th {
    background-color: #f7fafc;
    font-weight: 600;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>