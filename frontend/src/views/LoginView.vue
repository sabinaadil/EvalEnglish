<template>
  <div class="min-h-screen flex items-center justify-center bg-white p-4">
    <div class="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
      <h2 class="text-3xl font-bold text-center text-gray-800 mb-6">Кіру</h2>
      <div v-if="errors.length > 0" class="bg-red-100 text-red-700 p-4 rounded mb-4">
        <ul>
          <li v-for="error in errors" :key="error">{{ error }}</li>
        </ul>
      </div>
      <form @submit.prevent="submitForm" class="space-y-6">
        <div class="relative">
          <label for="email" class="block text-sm font-medium text-gray-700">Пошта</label>
          <div class="mt-1 relative">
            <input type="email" id="email" v-model="form.email" placeholder="Поштаңызды енгізіңіз"
              class="block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 transition duration-200"
              required />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="w-5 h-5 text-gray-400">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M16.5 12a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0Zm0 0c0 1.657 1.007 3 2.25 3S21 13.657 21 12a9 9 0 1 0-2.636 6.364M16.5 12V8.25" />
              </svg>

            </div>
          </div>
        </div>

        <div class="relative">
          <label for="password" class="block text-sm font-medium text-gray-700">Құпиясөз</label>
          <div class="mt-1 relative">
            <input type="password" id="password" v-model="form.password" placeholder="Құпиясөзді енгізіңіз"
              class="block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 transition duration-200"
              required />

            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="w-5 h-5 text-gray-400">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
              </svg>

            </div>
          </div>
        </div>

        <div>
          <button type="submit"
            class="w-full flex items-center justify-center px-4 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-5 h-5 mr-2">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="m12.75 15 3-3m0 0-3-3m3 3h-7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>

            Кіру
          </button>
        </div>
      </form>

      <div class="text-center mt-6">
        <p class="text-sm text-gray-600">
          Аккаунт жоқ па?
          <RouterLink to="/signup" class="text-blue-500 hover:underline font-medium transition duration-200">
            Осы жерде тіркеліңіз!
          </RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useToastStore } from '../stores/toast';
import { useUserStore } from '../stores/user'
import { useNotificationStore } from '../stores/notification';
import axios from 'axios'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const toastStore = useToastStore()
const router = useRouter()
const notificationStore = useNotificationStore();

const form = reactive({
  email: '',
  password: '',
})

const errors = ref([])

const submitForm = async () => {
  errors.value = []

  if (form.email === '') {
    errors.value.push('Поштаңызды еңгізу қажет!')
  }
  if (form.password === '') {
    errors.value.push('Құпиясөзді еңгізу қажет!')
  }

  if (errors.value.length === 0) {
    try {
      const response = await axios.post('/api/login/', form)

      userStore.setToken(response.data)
      axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access

      toastStore.showToast(3000, 'Сіз аккаунтыңызға сәтті кірдіңіз!', 'bg-emerald-500')

      const userInfoResponse = await axios.get('/api/me/')
      userStore.setUserInfo(userInfoResponse.data)

      // if (userStore.user.role === 'teacher' && userStore.user.isTeacher === false) {
      //   router.push({ name: 'teacher-application' })
      // } else {
      router.push({ name: 'home' })
      notificationStore.fetchUnreadCount();
      notificationStore.fetchPendingCount();
      // }

    } catch (error) {
      console.log('error', error)
      errors.value.push('Логин немесе құпиясөз қате!')
      errors.value.push('Мүмкін сіз аккаунтыңызды іске қоспадыңыз! Поштаңызды тексеруіңізді сұраймыз!')
    }
  }
}
</script>

<style scoped>
.transition {
  transition: all 0.3s ease;
}

input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
}

button:hover svg {
  transform: translateX(2px);
}
</style>
