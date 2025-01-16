<script setup>
import { onMounted, ref } from 'vue'
import Toast from './components/Toast.vue'
import { useUserStore } from './stores/user'
import axios from 'axios'

const userStore = useUserStore()
const pendingCount = ref(0)

onMounted(() => {
  if (userStore.user.is_superuser) {
    fetchPendingCount()
  }
})

function fetchPendingCount() {
  axios.get('/api/teacher-applications/pending_count/')
    .then(response => {
      pendingCount.value = response.data.count
    })
    .catch(err => {
      console.error(err)
      pendingCount.value = 0
    })
}
</script>

<template>
  <div class="h-screen flex flex-col overflow-hidden">
    <nav class="py-2 px-6 border-b bg-white flex-shrink-0">
      <div class="max-w-screen-2xl mx-auto flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <RouterLink to="/" class="text-blue-600 text-xl font-bold hover:text-blue-700">
            EvalEnglish
          </RouterLink>
        </div>

        <div class="flex items-center space-x-4">
          <div v-if="userStore.user.isSuperuser" class=" text-sm font-bold">
            <RouterLink :to="{ name: 'admin-notifications' }" class="hover:text-blue-700 transition">
              Заявки
              <span v-if="pendingCount > 0"
                class="ml-1 inline-block rounded-full bg-red-500 text-white text-xs px-1 leading-tight">
                {{ pendingCount }}
              </span>
            </RouterLink>
          </div>
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

    <main class="flex-1 overflow-auto bg-gray-50">
      <RouterView />
    </main>

    <Toast />
  </div>
</template>
