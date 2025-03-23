<template>
    <div>
        <h2 class="text-2xl font-bold mb-4">{{ lesson.title }}</h2>

        <!-- Если текущий шаг попадает в теорию -->
        <div v-if="currentStep <= lesson.pages.length" class="mb-6 text-gray-700 whitespace-pre-line">
            <p>{{ lesson.pages[currentStep - 1] }}</p>
        </div>

        <!-- Если текущий шаг соответствует вопросу -->
        <div v-else class="mb-6 text-gray-700">
            <p class="font-medium mb-2">
                Вопрос {{ currentStep - lesson.pages.length }}: {{ currentQuestion.text }}
            </p>
            <div class="space-y-2">
                <label v-for="(answer, index) in currentQuestion.answers" :key="index"
                    class="flex items-center space-x-2">
                    <input type="radio" :name="'question-' + currentStep" :value="answer" />
                    <span>{{ answer }}</span>
                </label>
            </div>
        </div>

        <!-- Кнопка "Далее" для перехода на следующий шаг (если нужна логика перехода) -->
        <button class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition mt-4">
            Далее
        </button>
    </div>
</template>

<script>
export default {
    name: "LessonContent",
    props: {
        lesson: {
            type: Object,
            required: true,
        },
        currentStep: {
            type: Number,
            required: true,
        },
    },
    computed: {
        currentQuestion() {
            const questionIndex = this.currentStep - this.lesson.pages.length - 1;
            return this.lesson.questions[questionIndex] || {};
        },
    },
};
</script>

<style scoped>
/* Дополнительные стили при необходимости */
</style>