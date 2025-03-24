<template>
    <div class="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow-lg">
        <h3 class="text-2xl font-bold text-blue-800 mb-6">1 қадам: Курсты ашу</h3>
        <div class="mb-6">
            <label class="block text-gray-700 font-medium mb-2" for="courseName">
                Курс атауы
            </label>
            <input id="courseName" v-model="localData.name" type="text" placeholder="Курс атауын еңгізіңіз..."
                class="w-full border border-gray-300 p-3 rounded focus:outline-none focus:border-blue-500 transition" />
        </div>
        <div class="mb-6">
            <label class="block text-gray-700 font-medium mb-2" for="courseDescription">
                Курс сипаттамасы
            </label>
            <textarea id="courseDescription" v-model="localData.description"
                placeholder="Курс сипаттамасын еңгізіңіз..."
                class="w-full border border-gray-300 p-3 rounded focus:outline-none focus:border-blue-500 transition"
                rows="5"></textarea>
        </div>
        <div class="flex justify-end">
            <button @click="$emit('next', localData)"
                class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg transition">
                Әрі қарай
            </button>
        </div>
    </div>
</template>

<script>
export default {
    name: "CreateCourseStep1",
    props: {
        formData: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            localData: {
                name: this.formData.name || "",
                description: this.formData.description || "",
            },
        };
    },
    watch: {
        localData: {
            handler(newVal) {
                this.$emit("update", newVal);
            },
            deep: true,
        },
    },
};
</script>

<style scoped>
/* Дополнительные стили можно добавить здесь */
</style>