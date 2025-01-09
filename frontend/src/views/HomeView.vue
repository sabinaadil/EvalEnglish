<template>
    <div v-if="user.isAuthenticated"
        class="flex flex-col items-center justify-center h-screen bg-gradient-to-br from-blue-100 via-white to-green-100">
        <h1 class="text-4xl font-extrabold text-blue-700 mb-6 text-center">
            <span class="text-green-600">EvalEnglish</span>-қа қош келдіңіз!😊
        </h1>
        <p class="text-lg text-gray-600 mb-8 text-center max-w-2xl">
            EvalEnglish
        </p>
        <RouterLink to="/"
            class="flex items-center justify-center px-6 py-3 bg-blue-500 text-white font-semibold rounded-lg shadow-lg hover:bg-blue-600 transition-all">
            <p class='text-xl ml-3'>EvalEnglish</p>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6 mb-5">
                <path stroke-linecap="round" stroke-linejoin="round"
                    d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z" />
            </svg>


        </RouterLink>

    </div>
</template>

<script>
import { useUserStore } from '../stores/user'

export default {
    name: 'Home',
    computed: {
        user() {
            const userStore = useUserStore()
            return userStore.user
        },
    },
    created() {
        if (!this.user.isAuthenticated) {
            this.$router.push({ name: 'login' })
        }
    },
}
</script>
