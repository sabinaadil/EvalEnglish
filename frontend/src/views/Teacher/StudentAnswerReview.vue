<template>
    <div class="container mx-auto p-6">
        <h1 class="text-3xl font-bold mb-8 text-center">Проверка ответов студента</h1>

        <!-- Карточка курса -->
        <div v-if="course" class="mb-8 p-6 border rounded-lg shadow-lg bg-white">
            <h2 class="text-2xl font-semibold text-blue-800">{{ course.name }}</h2>
            <p class="text-gray-700 mt-2">{{ course.description }}</p>
        </div>

        <!-- Карточка студента -->
        <div v-if="student" class="mb-8 p-6 border rounded-lg shadow-lg bg-white">
            <h3 class="text-xl font-semibold">
                {{ student.participant.first_name }} {{ student.participant.last_name }}
            </h3>
            <p class="text-gray-700 mt-1">{{ student.participant.email }}</p>
        </div>

        <!-- Секция вопросов и ответов -->
        <div>
            <h3 class="text-2xl font-semibold mb-6">Вопросы и ответы студента</h3>
            <div v-if="questions && questions.length">
                <div v-for="question in questions" :key="question.id"
                    class="mb-6 p-6 border rounded-lg shadow bg-gray-50">
                    <h4 class="text-lg font-bold text-gray-800 mb-2">
                        Вопрос: {{ question.question_text }}
                    </h4>
                    <p class="text-sm text-gray-500 mb-4">(ID: {{ question.id }})</p>

                    <div v-if="answersMap[question.id] && answersMap[question.id].length">
                        <div v-for="(ans, index) in answersMap[question.id]" :key="ans.id"
                            class="mb-4 pl-4 border-l-4 border-blue-300">
                            <p class="text-gray-800 mb-1">
                                <span class="font-semibold">Ответ {{ index + 1 }}:</span>
                                <em class="italic">{{ ans.answer_text }}</em>
                            </p>
                            <p class="text-gray-700 mb-1">
                                Время ответа: <span class="font-medium">{{ ans.time_spent }}</span> сек.
                            </p>
                            <p class="text-gray-700 mb-1">
                                Модельная оценка: <span class="font-medium">{{ ans.model_score }}</span>
                            </p>

                            <!-- Поле для оценки преподавателя -->
                            <div class="mb-2">
                                <label class="block text-gray-700 text-sm font-medium mb-1">
                                    Оценка преподавателя:
                                </label>
                                <input type="number" step="0.1" min="0" max="1" v-model.number="grades[ans.id]"
                                    class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500"
                                    placeholder="0.0" />
                            </div>

                            <button @click="updateGrade(ans)"
                                class="bg-blue-500 hover:bg-blue-600 text-white font-medium px-4 py-2 rounded transition duration-200">
                                Сохранить оценку
                            </button>
                        </div>
                    </div>
                    <div v-else class="text-gray-500">
                        Студент ещё не ответил на этот вопрос.
                    </div>
                </div>
            </div>
            <div v-else class="text-gray-500 text-center">
                Нет вопросов для отображения.
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "StudentAnswerReview",
    props: {
        courseId: {
            type: String,
            required: true,
        },
        studentId: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            course: null,
            student: null,
            questions: [],    // Массив вопросов типа text и file для курса
            answersMap: {},   // Объект вида { questionId: [answerObj, ...] }
            grades: {},       // Для хранения оценок преподавателя (ключ: answer.id)
        };
    },
    async created() {
        console.log("Входные параметры:", this.courseId, this.studentId);
        await this.fetchCourse();
        await this.fetchStudent();
        await this.fetchAnswers();
        // Если список вопросов пуст, пробуем извлечь их из modules
        if (!this.questions.length && this.course && this.course.modules) {
            this.extractQuestionsFromCourse();
        }
        console.log("Итоговый список вопросов:", this.questions);
        console.log("Итоговый answersMap:", this.answersMap);
    },
    methods: {
        async fetchCourse() {
            try {
                const response = await axios.get(`/api/course-detail/${this.courseId}/`);
                this.course = response.data;
                console.log("Курс получен:", this.course);
            } catch (error) {
                console.error("Ошибка загрузки курса:", error);
            }
        },
        extractQuestionsFromCourse() {
            const allQuestions = [];
            if (this.course && this.course.modules) {
                console.log("Модули курса:", this.course.modules);
                this.course.modules.forEach((mod) => {
                    if (mod.questions && mod.questions.length) {
                        mod.questions.forEach((q) => {
                            const qType = q.question_type ? q.question_type.toLowerCase() : "";
                            if (qType === "text" || qType === "file") {
                                allQuestions.push(q);
                            }
                        });
                    }
                });
            }
            this.questions = allQuestions;
            console.log("Извлечено вопросов из модулей:", this.questions);
        },
        async fetchStudent() {
            try {
                const response = await axios.get(`/api/course-participants/${this.courseId}/`);
                const participants = response.data;
                console.log("Все участники курса:", participants);
                // Если studentId – это ID записи CourseParticipant:
                this.student = participants.find((s) => s.id === this.studentId);
                // Если studentId – это ID пользователя:
                // this.student = participants.find((s) => s.participant.id === this.studentId);
                console.log("Найденный студент:", this.student);
            } catch (error) {
                console.error("Ошибка загрузки студента:", error);
            }
        },
        async fetchAnswers() {
            try {
                const response = await axios.get(`/api/student-answers/${this.studentId}/?course=${this.courseId}`);
                console.log("Ответ от API для ответов:", response.data);

                const answersArray = (response.data && Array.isArray(response.data.answers))
                    ? response.data.answers
                    : [];
                console.log("Массив ответов до фильтрации:", answersArray);

                // Фильтр по типу вопроса
                const filtered = answersArray.filter((ans) => {
                    if (ans.question_type) {
                        const qType = ans.question_type.toLowerCase();
                        return (qType === "text" || qType === "file");
                    } else {
                        // Если question_type нет, извлекаем его из question
                        const q = this.questions.find((q) => q.id === ans.question);
                        if (q && q.question_type) {
                            const qType = q.question_type.toLowerCase();
                            return (qType === "text" || qType === "file");
                        }
                        return false;
                    }
                });
                console.log("Отфильтрованные ответы:", filtered);

                const map = {};
                filtered.forEach((ans) => {
                    if (!map[ans.question]) {
                        map[ans.question] = [];
                    }
                    map[ans.question].push(ans);

                    // Используем teacher_score вместо score, чтобы не отображать результат модели
                    // или итоговый score. Если teacher_score отсутствует, ставим 0
                    const teacherScore = (ans.teacher_score !== null && ans.teacher_score !== undefined)
                        ? ans.teacher_score
                        : 0;
                    this.grades[ans.id] = teacherScore;
                });
                this.answersMap = map;

                // Если API возвращает вопросы отдельно, можно использовать их:
                if (response.data.questions && Array.isArray(response.data.questions)) {
                    this.questions = response.data.questions;
                    console.log("Вопросы получены из API:", this.questions);
                }

                console.log("Сформирован answersMap:", this.answersMap);
            } catch (error) {
                console.error("Ошибка загрузки ответов студента:", error);
            }
        },
        async updateGrade(answer) {
            try {
                const newGrade = this.grades[answer.id];
                await axios.post(`/api/user-answers/${answer.id}/grade/`, {
                    teacher_score: newGrade,
                });
                alert("Оценка сохранена.");
            } catch (error) {
                console.error("Ошибка обновления оценки:", error);
                alert("Ошибка обновления оценки. Попробуйте позже.");
            }
        },
        getQuestionText(questionId) {
            const question = this.questions.find((q) => q.id === questionId);
            return question ? question.question_text : questionId;
        },
    },
};
</script>

<style scoped>
table {
    border-collapse: collapse;
    width: 100%;
}

th,
td {
    padding: 0.75rem;
    text-align: left;
}
</style>