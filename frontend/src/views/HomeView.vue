<template>
    <div v-if="user.isAuthenticated"
        class="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-100 via-white to-green-100 p-4">
        <transition name="fade">
            <h1 v-if="user.isAuthenticated" class="text-5xl font-extrabold text-blue-700 mb-6 text-center">
                <span class="text-green-600">EvalEnglish</span>-қа қош келдіңіз!😊
            </h1>
        </transition>
        <transition name="slide-up">
            <p v-if="user.isAuthenticated" class="text-lg text-gray-600 mb-8 text-center max-w-2xl">
                Добро пожаловать в EvalEnglish — платформу для эффективного изучения английского языка. Начните свой
                путь к свободному владению языком уже сегодня!
            </p>
        </transition>
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

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.slide-up-enter-active {
    transition: all 0.5s ease;
}

.slide-up-enter-from {
    transform: translateY(20px);
    opacity: 0;
}

.scale-in-enter-active {
    transition: transform 0.3s ease, background-color 0.3s ease;
}

.scale-in-enter-from {
    transform: scale(0.95);
    opacity: 0;
}
</style>
