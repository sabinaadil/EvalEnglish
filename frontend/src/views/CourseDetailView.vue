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
                            Преподаватель: {{ course.teacherName }}
                        </span>
                    </div>

                    <div class="flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="w-5 h-5 text-gray-300">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M11.35 3.836c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m8.9-4.414c.376.023.75.05 1.124.08 1.131.094 1.976 1.057 1.976 2.192V16.5A2.25 2.25 0 0 1 18 18.75h-2.25m-7.5-10.5H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V18.75m-7.5-10.5h6.375c.621 0 1.125.504 1.125 1.125v9.375m-8.25-3 1.5 1.5 3-3.75" />
                        </svg>


                        <span class="text-gray-200">
                            {{ course.modulesCount }} модулей
                        </span>
                    </div>

                    <div class="flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="w-5 h-5 text-gray-300 ">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                        </svg>


                        <span class="text-gray-200">
                            {{ course.lessonsCount }} уроков
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <div class="container mx-auto px-4 py-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="md:col-span-2">
                    <h2 class="text-2xl font-semibold mb-4">Описание курса</h2>
                    <p class="text-gray-700 leading-relaxed">
                        {{ course.description }}
                    </p>

                    <h3 class="text-xl font-semibold mt-8 mb-3">
                        Чему вы научитесь
                    </h3>
                    <ul class="list-disc list-inside text-gray-700 space-y-1">
                        <li v-for="(item, index) in course.whatYouWillLearn" :key="index">
                            {{ item }}
                        </li>
                    </ul>
                </div>

                <div class="bg-gray-50 rounded-lg p-6 shadow-sm">
                    <button @click="$router.push({ name: 'CoursePlay', params: { id: '123' } })"
                        class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
                        Подписаться на курс
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
            required: true,
        },
    },
    data() {
        return {
            course: {
                title: "Английский для начинающих",
                subtitle:
                    "Научимся говорить на английском языке с нуля",
                teacherName: "Иван Иванов",
                modulesCount: 8,
                lessonsCount: 24,
                description: `
  Полное описание курса. Здесь можно подробно описать все темы, которые будут затронуты в курсе, а также навыки и знания, которые вы получите по окончании обучения. Можно добавлять различные детали, примеры и другие аспекты, чтобы пользователь понимал ценность курса и что именно он узнает.
          `,
                whatYouWillLearn: [
                    "Как правильно визуализировать данные",
                    "Качественной работе с легендами и цветовыми шкалами",
                    "Как создавать и комбинировать сложные графики",
                    "Работать с популярными библиотеками для визуализации",
                ],
            },
        };
    },
    mounted() {

    },
};
</script>

<style scoped></style>