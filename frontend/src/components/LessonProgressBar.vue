<template>
    <div class="flex space-x-2 p-3 border-b border-gray-200">
        <button v-for="step in totalSteps" :key="step" @click="selectStep(step)"
            class="w-6 h-6 flex items-center justify-center rounded border cursor-pointer transition-colors duration-200 text-xs"
            :class="{
                'bg-green-500 text-white border-green-500': step === currentStep,
                'bg-white text-gray-800 border-gray-300': step !== currentStep
            }">
            {{ step }}
        </button>
    </div>
</template>

<script>
export default {
    name: "LessonProgressBar",
    props: {
        totalSteps: {
            type: Number,
            required: true,
        },
        currentStep: {
            type: Number,
            required: true,
        },
    },
    methods: {
        selectStep(step) {
            this.$emit("stepSelected", step);
        },
    },
};
</script>

<style scoped>
/* Дополнительные стили, если необходимо */
</style>