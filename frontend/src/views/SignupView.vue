<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-white to-green-100 p-4">
    <div class="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
      <h2 class="text-3xl font-bold text-center text-gray-800 mb-6">Тіркелу</h2>

      <transition name="fade">
        <div v-if="errors.length > 0" class="bg-red-100 text-red-700 p-4 rounded mb-4">
          <ul>
            <li v-for="error in errors" :key="error" class="text-sm">{{ error }}</li>
          </ul>
        </div>
      </transition>

      <form @submit.prevent="submitForm" class="space-y-6">
        <div class="relative">
          <label for="first_name" class="block text-sm font-medium text-gray-700">Атыңыз</label>
          <input type="text" id="first_name" v-model="form.first_name" placeholder="Атыңызды енгізіңіз"
            class="mt-1 block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 transition duration-200" />
          <div class="absolute inset-y-0 left-0 pl-3 top-6 flex items-center pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-5 h-5 text-gray-400">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
            </svg>

          </div>
        </div>

        <div class="relative">
          <label for="last_name" class="block text-sm font-medium text-gray-700">Тегіңіз</label>
          <input type="text" id="last_name" v-model="form.last_name" placeholder="Тегіңізді енгізіңіз"
            class="mt-1 block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 transition duration-200" />
          <div class="absolute inset-y-0 left-0 pl-3 top-6 flex items-center pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-5 h-5 text-gray-400">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
            </svg>

          </div>
        </div>

        <div class="relative">
          <label for="email" class="block text-sm font-medium text-gray-700">Пошта</label>
          <input type="email" id="email" v-model="form.email" placeholder="Поштаңызды енгізіңіз"
            class="mt-1 block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 transition duration-200" />
          <div class="absolute inset-y-0 left-0 pl-3 top-6 flex items-center pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-5 h-5 text-gray-400">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M16.5 12a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0Zm0 0c0 1.657 1.007 3 2.25 3S21 13.657 21 12a9 9 0 1 0-2.636 6.364M16.5 12V8.25" />
            </svg>
          </div>
        </div>

        <div class="relative">
          <label for="password1" class="block text-sm font-medium text-gray-700">Құпиясөз</label>
          <input type="password" id="password1" v-model="form.password1" placeholder="Құпиясөзді енгізіңіз"
            class="mt-1 block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 transition duration-200" />
          <div class="absolute inset-y-0 left-0 pl-3 top-6 flex items-center pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-5 h-5 text-gray-400">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
            </svg>

          </div>
        </div>
        <div class="relative">
          <label for="password2" class="block text-sm font-medium text-gray-700">Құпиясөзді қайталаңыз</label>
          <input type="password" id="password2" v-model="form.password2" placeholder="Құпиясөзді растаңыз"
            class="mt-1 block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 transition duration-200" />
          <div class="absolute inset-y-0 left-0 pl-3 top-6 flex items-center pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-5 h-5 text-gray-400">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>

          </div>
        </div>
        <div class="flex items-center">
          <input type="checkbox" id="is_teacher_applicant" v-model="form.is_teacher_applicant"
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
          <label for="is_teacher_applicant" class="ml-2 block text-sm text-gray-700">
            Мен Оқытушымын
          </label>
        </div>
        <div>
          <button type="submit"
            class="w-full flex items-center justify-center px-4 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 animate-pulse" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Тіркелу
          </button>
        </div>
      </form>

      <div class="text-center mt-6">
        <p class="text-sm text-gray-600">
          Аккаунт бар ма?
          <RouterLink to="/login" class="text-blue-500 hover:underline font-medium transition duration-200">
            Мында басыңыз!
          </RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useToastStore } from '../stores/toast';
import { useRouter } from 'vue-router';
import axios from 'axios';

const toastStore = useToastStore();
const router = useRouter();

const form = reactive({
  email: '',
  first_name: '',
  last_name: '',
  password1: '',
  password2: '',
  is_teacher_applicant: false,
});

const errors = ref([]);

const isValidEmail = computed(() => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(form.email);
});

const submitForm = async () => {
  errors.value = [];

  if (form.first_name.trim() === '') {
    errors.value.push('Атыңызды еңгізу қажет!');
  }

  if (form.last_name.trim() === '') {
    errors.value.push('Тегіңізді еңгізу қажет!');
  }

  if (form.email.trim() === '') {
    errors.value.push('Поштаңызды еңгізу қажет!');
  } else if (!isValidEmail.value) {
    errors.value.push('Дұрыс поштаны еңгізу қажет!');
  }

  if (form.password1 === '') {
    errors.value.push('Құпиясөзді еңгізу қажет!');
  }

  if (form.password1 !== form.password2) {
    errors.value.push('Құпиясөздер сәйкес келмеді!');
  }

  if (errors.value.length === 0) {
    const payload = {
      email: form.email,
      first_name: form.first_name,
      last_name: form.last_name,
      password1: form.password1,
      password2: form.password2,
      is_teacher_applicant: form.is_teacher_applicant,
    };

    try {
      const response = await axios.post('/api/signup/', payload);

      if (response.data.message === 'success') {
        toastStore.showToast(3000, 'Аккаунт был создан. Проверьте почту для активации аккаунта.', 'bg-emerald-500');
        form.email = '';
        form.first_name = '';
        form.last_name = '';
        form.password1 = '';
        form.password2 = '';
        form.is_teacher_applicant = false;
        errors.value = [];
        router.push('/login');
      } else {
        errors.value = [];
        for (let field in response.data.message) {
          const fieldErrors = response.data.message[field];
          fieldErrors.forEach(msg => {
            errors.value.push(msg);
          });
        }
        toastStore.showToast(5000, 'Өкінішке орай бірдеңе дүрыс орындалмай қалды, кешірім сұраймыз!', 'bg-red-500');
      }
    } catch (error) {
      if (error.response) {
        console.error('Server Response:', error.response.data);
        errors.value.push('Ошибка сервера: ' + (error.response.data.message || 'Попробуйте позже.'));
      } else {
        errors.value.push('Тіркелу кезінде қате орын алды!');
      }
      toastStore.showToast(5000, 'Тіркелу кезінде қате орын алды!', 'bg-red-500');
    }
  }
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

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
