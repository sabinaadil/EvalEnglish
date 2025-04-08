<template>
    <div>
        <div class="bg-gray-800 text-white py-8 px-4 rounded-lg">
            <div class="container mx-auto">
                <h1 class="text-4xl font-bold mb-2">{{ course.title }}</h1>
                <p class="text-lg mb-4">{{ course.subtitle }}</p>
                <div class="flex flex-wrap items-center space-x-6 text-sm">
                    <div class="flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-300" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M5.121 17.804A4 4 0 019 16h6a4 4 0 013.879 1.804M12 12a4 4 0 100-8 4 4 0 000 8z" />
                        </svg>
                        <span class="text-gray-200">
                            Мұғалім: {{ course.teacherName }}
                        </span>
                    </div>

                    <div class="flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-300" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" />
                        </svg>
                        <span class="text-gray-200">
                            {{ course.modulesCount }} модульдер
                        </span>
                    </div>

                    <div class="flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-300" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                        </svg>
                        <span class="text-gray-200">
                            {{ course.lessonsCount }} сабақтар
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <div class="container mx-auto px-4 py-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="md:col-span-2">
                    <h2 class="text-2xl font-semibold mb-4">Курс сипаттамасы</h2>
                    <p class="text-gray-700 leading-relaxed">
                        {{ course.description }}
                    </p>

                    <h3 class="text-xl font-semibold mt-8 mb-3">
                        Не үйренесіз
                    </h3>
                    <ul class="list-disc list-inside text-gray-700 space-y-1">
                        <li v-for="(item, index) in course.whatYouWillLearn" :key="index">
                            {{ item }}
                        </li>
                    </ul>
                </div>

                <div class="bg-gray-50 rounded-lg p-6 shadow-sm">
                    <button @click="$router.push({ name: 'CoursePlay', params: { id: '123' } })"
                        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded">
                        Курсқа жазылу
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "CourseDetailView",
    props: {
        id: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            course: {
                title: "Ағылшын тілі – Бастапқы деңгей",
                subtitle: "Негізгі ағылшын курсы",
                teacherName: "Сабина Адилбекова",
                modulesCount: 8,
                lessonsCount: 24,
                description: `Курс туралы толық сипаттама. Мұнда курс тақырыптары, мақсаттары және сабақ мазмұны көрсетіледі. 
Мұғалімнің ұсынған әдістемесі мен практикалық тапсырмалары арқылы сіз ағылшын тілін тиімді меңгере аласыз.`,
                whatYouWillLearn: [
                    "Негізгі деңгейдегі тілдік қарым-қатынас дағдылары",
                    "Дұрыс айтылу және фонетика",
                    "Ағылшын тіліндегі негізгі уақыттар",
                    "Оқу және жазу дағдылары"
                ]
            }
        }
    },
    mounted() {
        // Локальді деректер негізінде курс объектісін орнатамыз
        // Бұл жерде серверге сұраныс жасалмайды, тек үлгі ретінде деректер қойылды.
    }
}
</script>

<style scoped>
/* Стилизация қажет болса қосыңыз */
</style>
