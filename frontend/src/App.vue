<script setup>
import Toast from './components/Toast.vue'
import { useUserStore } from './stores/user'

const userStore = useUserStore()
</script>

<template>
  <div class="h-screen flex flex-col overflow-hidden">
    <nav class="py-2 px-6 border-b bg-white flex-shrink-0">
      <div class="max-w-screen-2xl mx-auto flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <RouterLink to="/"
            class="text-blue-600 text-xl font-bold hover:text-blue-700 transition duration-300 ease-in-out">
            EvalEnglish
          </RouterLink>
        </div>
        <div class="flex items-center space-x-4">

          <template v-if="userStore.user.isAuthenticated">
            <RouterLink to="/">
              Вход выполнен
            </RouterLink>
          </template>
          <template v-if="userStore.user.isAuthenticated && userStore.user.id">
            <RouterLink :to="{ name: 'profile', params: { id: userStore.user.id } }">
              <img :src="userStore.user.avatar" class="w-[40px] h-[40px] object-cover rounded-full">
            </RouterLink>
          </template>
          <template v-else>
            <div class="text-sm font-bold">
              <RouterLink to="/login"
                class="text-green-600 rounded-lg mr-4 hover:text-blue-800 transition duration-300 ease-in-out">
                Кіру
              </RouterLink>
              <RouterLink to="/signup"
                class="text-white bg-blue-600 py-2 px-3 rounded-lg hover:bg-blue-700 transition duration-300 ease-in-out">
                Тіркелу
              </RouterLink>
            </div>
          </template>
        </div>
      </div>
    </nav>
    <main class="flex-1 overflow-auto bg-gray-50">
      <RouterView />
    </main>

    <Toast />
  </div>
</template>
