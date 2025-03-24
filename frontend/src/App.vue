<script setup>
import { onMounted, ref } from 'vue';
import Toast from './components/Toast.vue';
import { useUserStore } from './stores/user';
import { useNotificationStore } from './stores/notification';

const userStore = useUserStore();
const notificationStore = useNotificationStore();

onMounted(() => {
  notificationStore.fetchUnreadCount();
  if (userStore.user.isSuperuser) {
    notificationStore.fetchPendingCount();
  }
});
</script>

<template>
  <!-- Основной контейнер экрана -->
  <div class="h-screen flex flex-col">
    <!-- Шапка (header) -->
    <nav class="py-2 px-6 border-b bg-white flex-shrink-0">
      <div class="max-w-screen-2xl mx-auto flex items-center justify-between">
        <!-- Логотип -->
        <div class="flex items-center space-x-4">
          <RouterLink to="/" class="text-blue-600 text-xl font-bold hover:text-blue-700">
            EvalEnglish
          </RouterLink>
        </div>

        <!-- Правая часть шапки -->
        <div class="flex items-center space-x-4">
          <!-- Если пользователь - преподаватель, показываем кнопку "Создать курс" -->
          <div v-if="userStore.user.isTeacher">
            <RouterLink to="/teacher/courses" class=" text-gray-600 py-2 px-3 font-bold rounded">
              Оқытушы кабинеті
            </RouterLink>
          </div>
          <div>
            <RouterLink to="/teacher/courses" class=" text-gray-600 py-2 px-3 font-bold rounded">
              Менің оқуым
            </RouterLink>
          </div>

          <!-- Уведомления для авторизованного пользователя -->
          <div v-if="userStore.user.isAuthenticated" class="relative text-md font-bold">
            <RouterLink :to="{ name: 'notifications' }" class="hover:text-blue-700 transition flex items-center gap-2">
              <!-- Иконка -->
              <span class="text-gray-600">Хабарламалар</span>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022
             c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
              </svg>

              <!-- Текст -->

            </RouterLink>

            <!-- Счётчик уведомлений -->
            <span v-if="notificationStore.unreadCount > 0"
              class="absolute top-0 right-0 -mt-2 -mr-2 inline-block rounded-full bg-red-500 text-white text-xs px-2 leading-tight">
              {{ notificationStore.unreadCount }}
            </span>
          </div>


          <!-- Админ-уведомления -->
          <div v-if="userStore.user.isSuperuser" class="relative text-sm font-bold">
            <RouterLink :to="{ name: 'admin-notifications' }" class="hover:text-blue-700 transition">
              <!-- Иконка админ-уведомлений -->
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 0 1-1.043 3.296
                         3.745 3.745 0 0 1-3.296 1.043A3.745 3.745 0 0 1 12 21c-1.268 0-2.39-.63-3.068-1.593
                         a3.746 3.746 0 0 1-3.296-1.043 3.745 3.745 0 0 1-1.043-3.296A3.745 3.745 0 0 1 3 12
                         c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 0 1 1.043-3.296 3.746 3.746 0 0 1 3.296-1.043
                         A3.746 3.746 0 0 1 12 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 0 1 3.296 1.043
                         3.746 3.746 0 0 1 1.043 3.296A3.745 3.745 0 0 1 21 12Z" />
              </svg>
            </RouterLink>
            <!-- Счётчик админ-уведомлений -->
            <span v-if="notificationStore.pendingCount > 0"
              class="absolute top-0 right-0 -mt-2 -mr-2 inline-block rounded-full bg-red-500 text-white text-xs px-2 leading-tight">
              {{ notificationStore.pendingCount }}
            </span>
          </div>

          <!-- Аватарка пользователя или кнопки входа -->
          <template v-if="userStore.user.isAuthenticated && userStore.user.id">
            <RouterLink :to="{ name: 'profile', params: { id: userStore.user.id } }">
              <img :src="userStore.user.avatar" class="w-[40px] h-[40px] object-cover rounded-full">
            </RouterLink>
          </template>
          <template v-else>
            <div class="text-sm font-bold">
              <RouterLink to="/login" class="text-green-600 rounded-lg mr-4 hover:text-blue-800">
                Кіру
              </RouterLink>
              <RouterLink to="/signup" class="text-white bg-blue-600 py-2 px-3 rounded-lg hover:bg-blue-700">
                Тіркелу
              </RouterLink>
            </div>
          </template>
        </div>
      </div>
    </nav>

    <!-- Основной контент (RouterView) -->
    <main class="flex-1 bg-gray-50 overflow-auto">
      <!-- Контейнер для ограничения ширины контента -->
      <div class="max-w-screen-xl mx-auto px-4 py-6">
        <RouterView />
      </div>
    </main>

    <!-- Компонент всплывающих уведомлений -->
    <Toast />
  </div>
</template>
