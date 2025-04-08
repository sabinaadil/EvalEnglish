<template>
    <div class="max-w-3xl mx-auto px-6 py-8">
        <!-- Заголовок урока -->
        <h2 class="text-3xl font-bold text-blue-800 mb-6 text-center">
            {{ lesson.title }}
        </h2>

        <!-- Прогресс-бары -->
        <div class="w-full bg-gray-300 rounded-full h-3 mb-4">
            <div class="bg-green-500 h-3 rounded-full transition-all duration-500" :style="{ width: progress + '%' }">
            </div>
        </div>
        <p class="text-sm text-gray-600 mb-6 text-center">
            Қазіргі жетістік: {{ currentStep }} / {{ totalSteps }} қадам ({{ progress }}%)
        </p>

        <!-- Теория беттері -->
        <div v-if="currentStep <= lesson.pages.length" class="mb-8">
            <div class="p-6 bg-gray-50 rounded-lg shadow">
                <h3 class="text-xl font-semibold mb-4">
                    Теория, бет {{ currentStep }}
                </h3>
                <p class="text-gray-700 whitespace-pre-line leading-relaxed">
                    {{ lesson.pages[currentStep - 1] }}
                </p>
            </div>
        </div>

        <!-- Сұрақ беттері -->
        <div v-else-if="currentStep < totalSteps" class="mb-8">
            <div class="p-6 bg-gray-50 rounded-lg shadow">
                <h3 class="text-xl font-semibold mb-4">
                    Сұрақ {{ currentStep - lesson.pages.length }}
                </h3>
                <p class="text-gray-700 mb-4 font-medium">
                    {{ currentQuestion.text }}
                </p>
                <p class="text-sm text-gray-600 mb-2">Жауапты мұқият таңдаңыз:</p>
                <div class="space-y-3">
                    <label v-for="(answer, index) in currentQuestion.answers" :key="index"
                        class="flex items-center space-x-3">
                        <input type="radio" :name="'question-' + currentStep" :value="answer"
                            class="form-radio text-green-500" />
                        <span class="text-gray-800">{{ answer }}</span>
                    </label>
                </div>
                <p class="text-xs text-gray-500 mt-3">
                    Ескерту: Сіздің жауабыңыз жүйе бойынша бағаланады.
                </p>
            </div>
        </div>

        <!-- Финалдық бет (currentStep === totalSteps) -->
        <div v-else class="mb-8 text-center">
            <div class="inline-block p-10 bg-green-100 rounded-lg shadow text-center max-w-lg mx-auto">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20 mx-auto text-green-600 mb-4" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
                <p class="font-bold text-3xl text-green-700 mb-2">
                    Дұрыс жауап, Сіз кереметсіз!
                </p>
                <p class="text-gray-700 mb-4">
                    Курсты аяқтағаныңызға рақмет. Сіз сабақтың маңызды бөлімдерін меңгердіңіз.
                </p>
                <a href="#" class="text-blue-500 underline text-lg">
                    Аналитикаға өту
                </a>
            </div>
        </div>

        <!-- "Келесі" батырмасы (егер currentStep < totalSteps) -->
        <div v-if="currentStep < totalSteps" class="flex justify-end">
            <button @click="$emit('next')"
                class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg transition">
                Келесі
            </button>
        </div>
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
        totalSteps: {
            type: Number,
            required: true,
        },
    },
    computed: {
        progress() {
            return Math.round((this.currentStep / this.totalSteps) * 100);
        },
        currentQuestion() {
            // questionIndex = текущий шаг минус количество теоретических страниц, минус 1
            const questionIndex = this.currentStep - this.lesson.pages.length - 1;
            return this.lesson.questions[questionIndex] || {};
        },
    },
};
</script>

<style scoped>
/* Қажет болса қосымша стильдер */
</style>