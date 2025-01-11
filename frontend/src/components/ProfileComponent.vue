<template>
    <div
        class="h-screen flex flex-col justify-center items-center bg-gradient-to-br from-blue-200 via-white to-gray-100 p-6">
        <div class="bg-white p-8 rounded-lg shadow-2xl max-w-md w-full space-y-6">
            <div class="flex flex-col items-center mb-4">
                <RouterLink :to="{ name: 'profile', params: { id: user.id } }" class="flex flex-col items-center group">
                    <div class="relative">
                        <img :src="user.avatar || '/default-avatar.png'" alt="Аватар пользователя"
                            class="w-28 h-28 rounded-full object-cover border-4 border-blue-500 group-hover:shadow-lg transition-shadow duration-300" />
                        <div v-if="userStore.user.id === user.id"
                            class="absolute bottom-0 right-0 transform translate-x-1/4 translate-y-1/4 bg-blue-600 text-white p-1 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-4 h-4">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M16.862 4.487l1.688-1.688a1.5 1.5 0 1 1 2.122 2.122L7.122 18.471a4.5 4.5 0 0 1-1.897 1.13l-2.686.8.8-2.686a4.5 4.5 0 0 1 1.13-1.897L16.862 4.487z" />
                            </svg>
                        </div>
                    </div>
                    <h2
                        class="mt-4 text-2xl font-bold text-blue-600 group-hover:underline transition-colors duration-300">
                        {{ (user.firstName + ' ' + user.lastName) || 'Без имени' }}
                    </h2>
                </RouterLink>
                <p class="text-gray-500 mt-1 text-sm">{{ user.email || 'Нет email' }}</p>
            </div>

            <div class="grid grid-cols-2 gap-4">
                <button @click="logout"
                    class="w-full px-4 py-2 bg-red-500 text-white font-semibold rounded-lg hover:bg-red-600 transition-colors flex items-center justify-center space-x-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
                    </svg>

                    <span>Шығу</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { useUserStore } from '../stores/user'
import axios from 'axios'
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
    name: 'ProfileComponent',
    setup() {
        const userStore = useUserStore()
        const router = useRouter()

        const user = userStore.user

        const logout = () => {
            userStore.removeToken()
            router.push({ name: 'login' })
        }

        const goToPreferencesSurvey = () => {
            router.push({ name: 'PreferencesSurvey' })
        }

        return {
            user,
            logout,
            userStore
        }
    }
}
</script>

<style scoped></style>
