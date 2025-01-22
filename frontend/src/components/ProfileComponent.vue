<template>
    <div class="max-w-md mx-auto bg-white p-8 mt-10 shadow rounded-lg space-y-6">
        <h1 class="text-2xl font-bold text-center">Сіздің профиліңіз</h1>
        <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded mb-4">
            {{ error }}
        </div>
        <div v-if="message" class="bg-green-100 text-green-700 p-4 rounded mb-4">
            {{ message }}
        </div>
        <div v-if="user" class="space-y-2">
            <div class="flex items-center justify-center">
                <img :src="user.avatar" alt="Avatar"
                    class="w-24 h-24 object-cover rounded-full border border-gray-300" />
            </div>
            <p class="text-center">
                <strong>Логин:</strong> {{ user.first_name }} {{ user.last_name }}
            </p>
            <p class="text-center">
                <strong>Пошта:</strong> {{ user.email }}
            </p>
            <p v-if="user.is_superuser" class="text-center">
                <strong>Рөл: </strong>
                <span class="capitalize">Әкімші</span>
            </p>
            <p v-else class="text-center">
                <strong>Рөл: </strong>
                <span class="capitalize">{{ translatedRole }}</span>
            </p>
            <RouterLink :to="{ name: 'teacher-application' }">
                <div v-if="!user.is_superuser && user.role !== 'student'"
                    class="flex items-center justify-center mt-4 p-4 bg-white border border-gray-200 rounded-lg shadow-md hover:bg-blue-50 transition duration-300 cursor-pointer">
                    <strong class="text-gray-800 mr-2">Оқытушы мәртебесі:</strong>
                    <span :class="statusClass">
                        {{ translatedStatus }}
                    </span>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2 text-blue-600" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                </div>
            </RouterLink>
        </div>

        <div class="text-center">
            <button @click="toggleEditForm"
                class="px-4 py-2 bg-blue-500 text-white rounded shadow hover:bg-blue-600 transition-colors">
                {{ isEditFormVisible ? 'Форманы жасыру' : 'Профиль деректерін өзгерту' }}
            </button>
        </div>

        <transition name="fade">
            <form v-if="isEditFormVisible" @submit.prevent="submitForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">Аты</label>
                    <input type="text" v-model="form.first_name"
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2"
                        placeholder="Атыңызды енгізіңіз" />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700">Тегі</label>
                    <input type="text" v-model="form.last_name"
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2"
                        placeholder="Тегіңізді енгізіңіз" />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700">Пошта</label>
                    <input type="email" v-model="form.email"
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2"
                        placeholder="Поштаңызды енгізіңіз" />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700">Аватар</label>
                    <input type="file" @change="handleFileChange" accept="image/*" class="mt-1 block w-full text-sm text-gray-500
                           file:mr-4 file:py-2 file:px-4
                           file:rounded-md file:border-0
                           file:text-sm file:font-semibold
                           file:bg-blue-50 file:text-blue-700
                           hover:file:bg-blue-100" />
                </div>

                <button type="submit"
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors">
                    Профильді жаңарту
                </button>
            </form>
        </transition>

        <div class="text-center">
            <button @click="logout"
                class="px-4 py-2 bg-red-600 text-white rounded-md shadow hover:bg-red-700 transition-colors">
                Шығу
            </button>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const user = ref(null)
const error = ref('')
const message = ref('')

const isEditFormVisible = ref(false)

const form = reactive({
    first_name: '',
    last_name: '',
    email: '',
    avatar: null,
})

const statusClass = computed(() => {
    return user.value.is_teacher ? 'text-green-600 font-semibold' : 'text-gray-600 font-semibold'
})

const roleMap = {
    'student': 'Студент',
    'teacher': 'Оқытушы',
    'admin': 'Әкімші',
}

const statusMap = {
    'pending': 'Күтілуде',
    'approved': 'Расталды',
    'rejected': 'Қабылданбады',
}

const translatedRole = computed(() => {
    return roleMap[user.value?.role] || user.value?.role
})

const translatedStatus = computed(() => {
    return statusMap[user.value?.status] || (user.value?.is_teacher ? 'Расталды' : 'Расталған жоқ')
})

function getUserInfo() {
    axios.get('/api/me/')
        .then(res => {
            user.value = res.data
            form.first_name = user.value.first_name
            form.last_name = user.value.last_name
            form.email = user.value.email
        })
        .catch(err => {
            error.value = err.response?.data?.detail || 'Ошибка при получении информации'
        })
}

function handleFileChange(event) {
    const file = event.target.files[0]
    if (file) {
        form.avatar = file
    }
}
function logout() {
    userStore.logout()
    router.push({ name: 'login' })
}

function submitForm() {
    error.value = ''
    message.value = ''

    const fd = new FormData()
    fd.append('first_name', form.first_name)
    fd.append('last_name', form.last_name)
    fd.append('email', form.email)

    if (form.avatar) {
        fd.append('avatar', form.avatar)
    }

    axios.post('/api/editprofile/', fd, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
        .then(res => {
            message.value = 'Профиль сәтті жаңартылды!'

            user.value = res.data.user

            userStore.setUserInfo(res.data.user)

            form.avatar = null
            isEditFormVisible.value = false
        })
        .catch(err => {
            error.value = err.response?.data?.message || 'Ошибка при обновлении профиля'
        })
}

function toggleEditForm() {
    isEditFormVisible.value = !isEditFormVisible.value
}

onMounted(() => {
    getUserInfo()
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: all 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}
</style>
