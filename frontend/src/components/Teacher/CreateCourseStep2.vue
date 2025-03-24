<template>
    <div class="max-w-3xl mx-auto bg-white p-8 rounded-lg shadow-lg">
        <h3 class="text-2xl font-bold text-blue-800 mb-6">
            2 қадам: Курс модульдерін қосу «{{ formData.name }}»
        </h3>

        <div v-if="localModules.length === 0" class="text-gray-600 mb-6">
            Әлі модульдер қосылмаған!
        </div>

        <div v-for="(module, index) in localModules" :key="index" class="mb-6 border border-gray-200 p-6 rounded-lg">
            <div class="flex items-center justify-between mb-4">
                <h4 class="text-lg font-semibold text-gray-800">
                    Модуль №{{ index + 1 }}
                </h4>
                <span class="text-sm text-gray-500">Реті: {{ module.order }}</span>
            </div>
            <div class="mb-4">
                <label class="block text-gray-700 font-medium mb-2" for="moduleTitle">Модуль атауы</label>
                <input id="moduleTitle" v-model="module.title" type="text" placeholder="Модуль атауын еңгізіңіз..."
                    class="w-full border border-gray-300 p-3 rounded-lg focus:outline-none focus:border-blue-500 transition" />
            </div>
            <div class="mb-4">
                <label class="block text-gray-700 font-medium mb-2" for="moduleDescription">Модуль сипаттамасы</label>
                <textarea id="moduleDescription" v-model="module.description"
                    placeholder="Модуль сипаттамасын еңгізіңіз..."
                    class="w-full border border-gray-300 p-3 rounded-lg focus:outline-none focus:border-blue-500 transition"
                    rows="4"></textarea>
            </div>
        </div>

        <button @click="addModule"
            class="bg-green-500 hover:bg-green-600 text-white font-semibold px-5 py-3 rounded-lg shadow transition mb-6">
            Модульді қосу
        </button>

        <div class="flex justify-between">
            <button @click="$emit('back')"
                class="bg-gray-500 hover:bg-gray-600 text-white font-medium px-5 py-3 rounded-lg transition">
                Артқа
            </button>
            <button @click="emitNext"
                class="bg-blue-500 hover:bg-blue-600 text-white font-medium px-5 py-3 rounded-lg transition">
                Әрі қарай
            </button>
        </div>
    </div>
</template>

<script>
export default {
    name: "CreateCourseStep2",
    props: {
        formData: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            localModules: this.formData.modules || [],
        };
    },
    methods: {
        addModule() {
            this.localModules.push({
                title: "",
                description: "",
                order: this.localModules.length + 1,
                due_date: null,
            });
        },
        emitNext() {
            this.$emit("next", { modules: this.localModules });
        },
    },
    watch: {
        localModules: {
            handler(newVal) {
                // Передаем изменения наверх для актуализации formData
                this.$emit("update", { modules: newVal });
            },
            deep: true,
        },
    },
};
</script>

<style scoped>
/* Дополнительные стили можно добавить по необходимости */
</style>