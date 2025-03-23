<template>
    <div class="p-6 max-w-screen-lg mx-auto">
        <h1 class="text-2xl font-bold mb-4">Создать курс</h1>
        <form @submit.prevent="createCourse" enctype="multipart/form-data">
            <div class="mb-4">
                <label class="block text-sm font-medium mb-2">Название курса</label>
                <input v-model="course.name" type="text" class="w-full border rounded px-4 py-2" required />
            </div>
            <div class="mb-4">
                <label class="block text-sm font-medium mb-2">Описание курса</label>
                <textarea v-model="course.description" class="w-full border rounded px-4 py-2" required></textarea>
            </div>
            <div class="mb-4">
                <label class="block text-sm font-medium mb-2">Загрузить изображение (по желанию)</label>
                <input type="file" @change="handleFileChange" class="w-full border rounded px-4 py-2" />
            </div>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Создать</button>
        </form>

        <!-- Ошибки -->
        <div v-if="errorMessage" class="mt-4 text-red-600">
            <p>{{ errorMessage }}</p>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/user";

export default {
    data() {
        return {
            course: {
                name: "",
                description: "",
                image: null, // Если вы хотите загрузить файл
            },
            errorMessage: "", // Для хранения ошибок
        };
    },
    methods: {
        handleFileChange(event) {
            // Обработчик изменения файла
            const file = event.target.files[0];
            if (file) {
                this.course.image = file;
            }
        },
        async createCourse() {
            const userStore = useUserStore(); // Получаем доступ к store пользователя
            const formData = new FormData();
            formData.append("name", this.course.name);
            formData.append("description", this.course.description);
            formData.append("teacher", userStore.user.id); // Добавляем ID преподавателя
            formData.append("created_at", new Date().toISOString()); // Устанавливаем текущую дату

            if (this.course.image) {
                formData.append("image", this.course.image);
            }

            try {
                const response = await axios.post("/api/courses/", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                });

                this.$router.push({ name: "home" });
            } catch (error) {
                if (error.response && error.response.data) {
                    // Вывод ошибок с сервера
                    this.errorMessage = error.response.data.error || "Произошла ошибка при создании курса.";
                } else {
                    this.errorMessage = "Произошла ошибка при отправке данных.";
                }
            }
        },
    },
};
</script>


<style scoped>
/* Можно добавить стиль для ошибок или загрузки */
</style>
