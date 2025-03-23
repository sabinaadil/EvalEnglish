<template>
    <!-- Оборачиваем всю карточку в router-link для кликабельности -->
    <router-link :to="`/courses/${course.id}`" class="block">
        <div
            class="bg-white rounded-lg overflow-hidden shadow hover:shadow-xl transform hover:scale-105 transition duration-300 cursor-pointer">
            <!-- Изображение курса -->
            <div class="h-40 bg-gray-200 flex items-center justify-center">
                <span class="text-gray-500 text-xs">Изображение курса</span>
            </div>
            <div class="p-4">
                <!-- Название курса -->
                <h2 class="text-sm font-semibold mb-2 line-clamp-2">
                    {{ course.name }}
                </h2>
                <!-- Описание курса -->
                <p class="text-xs text-gray-600 line-clamp-3">
                    {{ course.description }}
                </p>
                <!-- Имя преподавателя -->
                <p class="text-xs text-gray-500 mt-2">
                    Преподаватель: {{ course.teacher_name }}
                </p>
            </div>
        </div>
    </router-link>
</template>

<script>
export default {
    name: "CourseCard",
    props: {
        course: {
            type: Object,
            required: true,
        },
    },
};
</script>

<style scoped>
/* Обрезка текста на 2 строки для заголовка */
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Обрезка текста на 3 строки для описания */
.line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>
