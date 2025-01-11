<script setup>
import { ref, reactive } from 'vue';
import { useToastStore } from '../stores/toast';
import { useRouter } from 'vue-router';
import axios from 'axios';

const toastStore = useToastStore();
const router = useRouter();

const form = reactive({
  email: '',
  firstName: '',
  lastName: '',
  password1: '',
  password2: '',
});

const errors = ref([]);

const submitForm = () => {
  errors.value = [];

  if (form.firstName === '') {
    errors.value.push('Вы пропустили имя!');
  }

  if (form.lastName === '') {
    errors.value.push('Вы пропустили фамилию!');
  }

  if (form.email === '') {
    errors.value.push('Вы пропустили email!');
  }

  if (form.password1 === '') {
    errors.value.push('Вы пропустили пароль!');
  }

  if (form.password1 !== form.password2) {
    errors.value.push('Пароли не совпадают!');
  }

  if (errors.value.length === 0) {
    axios
      .post('/api/signup/', form)
      .then(response => {
        if (response.data.message === 'success') {
          toastStore.showToast(3000, 'Аккаунт был создан. Теперь вам необходимо активировать аккаунт!', 'bg-emerald-500');
          form.email = '';
          form.firstName = '';
          form.lastName = '';
          form.password1 = '';
          form.password2 = '';
          router.push('/login');

          errors.value = [];
        } else {
          errors.value = [];
          for (let field in response.data.message) {
            const fieldErrors = response.data.message[field];
            fieldErrors.forEach(msg => {
              errors.value.push(msg);
            });
          }
          toastStore.showToast(5000, 'Что-то пошло не так, попробуйте ещё раз!', 'bg-red-500');
        }
      })
      .catch(error => {
        console.error('An error occurred:', error);
        errors.value.push('Произошла ошибка при регистрации!');
        toastStore.showToast(5000, 'Произошла ошибка при регистрации!', 'bg-red-500');
      });
  }
};

</script>

<template>
  <div class="max-w-screen-2xl mx-auto grid grid-cols-5 gap-4 text-sm text-black mt-10">
    <div class="main-left col-span-3 ml-4">
      <div class="p-12 bg-white shadow-lg rounded-lg">
        <h1 class="mb-6 text-2xl">EvalEnglish</h1>
        <div>
          <label class="font-medium">test</label><br>
          <div class="relative mt-2">

            <div class="flex flex-wrap mb-2">

            </div>
          </div>
        </div>
        <br>
        <p class="font-bold mb-4">
          Аккаунт бар ма? <RouterLink :to="{ 'name': 'login' }"
            class="text-blue-600 hover:text-blue-800 transition duration-300 ease">
            Мында басыңыз!</RouterLink>
        </p>
      </div>
    </div>
    <div class="main-center col-span-2 space-y-4 mr-4">
      <div class="p-12 bg-white shadow-lg rounded-lg">
        <form class="space-y-6" v-on:submit.prevent="submitForm">
          <div>
            <label>Атыңыз</label><br>
            <input type="text" v-model="form.firstName" placeholder="Атыңызды енгізіңіз"
              class="w-full mt-2 py-4 px-6 border border-gray-400 rounded-lg bg-gray-100 text-black placeholder-gray-500">
          </div>
          <div>
            <label>Тегіңіз</label><br>
            <input type="text" v-model="form.lastName" placeholder="Тегіңізді енгізіңіз"
              class="w-full mt-2 py-4 px-6 border border-gray-400 rounded-lg bg-gray-100 text-black placeholder-gray-500">
          </div>
          <div>
            <label>Пошта</label><br>
            <input type="email" v-model="form.email" placeholder="Поштаңызды енгізіңіз"
              class="w-full mt-2 py-4 px-6 border border-gray-400 rounded-lg bg-gray-100 text-black placeholder-gray-500">
          </div>
          <div>
            <label>Құпиясөз</label><br>
            <input type="password" v-model="form.password1" placeholder="Құпиясөзді енгізіңіз"
              class="w-full mt-2 py-4 px-6 border border-gray-400 rounded-lg bg-gray-100 text-black placeholder-gray-500">
          </div>
          <div>
            <label>Құпиясөзді қайталаңыз</label><br>
            <input type="password" v-model="form.password2" placeholder="Құпиясөзді растаңыз"
              class="w-full mt-2 py-4 px-6 border border-gray-400 rounded-lg bg-gray-100 text-black placeholder-gray-500">
          </div>

          <template v-if="errors.length > 0">
            <div class="bg-red-500 p-4 rounded-lg text-white">
              <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>
          </template>
          <div>
            <button
              class="font-bold w-full py-4 px-6 bg-blue-500 text-white rounded-lg hover:bg-blue-700 transition duration-300 ease">Тіркелу</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>



<style scoped></style>
