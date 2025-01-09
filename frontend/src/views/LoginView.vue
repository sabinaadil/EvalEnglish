<script>
import { useToastStore } from '../stores/toast';
import { useUserStore } from '../stores/user'
import axios from 'axios'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const userStore = useUserStore()
    const toastStore = useToastStore()
    const router = useRouter()

    const form = reactive({
      email: '',
      password: '',
    })

    const errors = ref([])

    const submitForm = async () => {
      errors.value = []

      if (form.email === '') {
        errors.value.push('Вы пропустили email!')
      }

      if (form.password === '') {
        errors.value.push('Вы пропустили пароль!')
      }

      if (errors.value.length === 0) {
        try {
          const response = await axios.post('/api/login/', form)

          userStore.setToken(response.data)
          axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access

          toastStore.showToast(3000, 'Вы успешно вошли в аккаунт!', 'bg-emerald-500')

          const userInfoResponse = await axios.get('/api/me/')

          userStore.setUserInfo(userInfoResponse.data)

          router.push({ name: 'home' })


        } catch (error) {
          console.log('error', error)
          errors.value.push('Неправильный логин или пароль! ')
          errors.value.push('Проверьте почту, если вы еще не активировали аккаунт! ')
        }
      }
    }


    return {
      form,
      errors,
      submitForm
    }
  }
}
</script>

<template>
  <div class="max-w-screen-2xl mt-10 mx-auto grid grid-cols-5 gap-4 text-sm">
    <div class="main-left col-span-3 ml-4">
      <div class="p-8 bg-white shadow-lg rounded-lg">
        <h1 class="mb-6 text-2xl">Кіру</h1>
        <p class="text-xl mb-6 text-gray-500">
          EvalEnglish
        </p>
        <p class="font-bold mb-4">
          Аккаунт жоқ па?
          <RouterLink :to="{ 'name': 'signup' }" class="text-blue-500 hover:text-blue-700 transition duration-300 ease">
            Тіркеліңіз!
          </RouterLink>
          Сол кезде біздің ұсыныстарға мүмкіндік аласыз!
        </p>
      </div>
    </div>
    <div class="main-center col-span-2 space-y-4 mr-4">
      <div class="p-8 bg-white shadow-lg rounded-lg">
        <form class="space-y-6" v-on:submit.prevent="submitForm">
          <div>
            <label>Пошта</label><br>
            <input type="email" v-model="form.email" placeholder="Поштаны енгізіңіз"
              class="w-full mt-2 py-4 px-6 border border-gray-400 rounded-lg bg-white text-black placeholder-gray-400">
          </div>
          <div>
            <label>Құпиясөз</label><br>
            <input type="password" v-model="form.password" placeholder="Құпиясөзді енгізіңіз"
              class="w-full mt-2 py-4 px-6 border border-gray-400 rounded-lg bg-white text-black placeholder-gray-400">
          </div>
          <template v-if="errors.length > 0">
            <div class="bg-red-500 p-4 rounded-lg text-white">
              <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>
          </template>
          <div>
            <button
              class="font-bold w-full py-4 px-6 bg-blue-500 text-white rounded-lg hover:bg-blue-700 transition duration-300 ease">Войти</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>




<style scoped></style>