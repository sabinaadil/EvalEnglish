<template>
    <div
        class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-white to-green-100 p-4">
        <div class="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
            <h2 class="text-3xl font-bold text-center text-gray-800 mb-6">Хабарламалар</h2>

            <div v-if="loading" class="text-center text-gray-600">
                Хабарламаларды жүктеу...
            </div>

            <div v-else>
                <div v-if="notifications.length === 0" class="text-center text-gray-600">
                    Сізде хабарламалар жоқ.
                </div>
                <ul v-else class="space-y-4 ">
                    <li v-for="notification in notifications" :key="notification.id"
                        class="p-4 rounded-lg transition ease-in-out duration-300"
                        :class="notification.read ? 'bg-gray-100' : 'bg-blue-50 border-l-4 border-blue-500'">
                        <p class="text-gray-700">{{ notification.message }}</p>
                        <p class="text-sm text-gray-500 mt-1 flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-4 h-4 mr-1">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                            {{ formatTime(notification.created_at) }}
                        </p>

                        <div v-if="notification.action_url" class="mt-2">
                            <a :href="notification.action_url" class="text-blue-500 hover:underline"
                                @click.prevent="handleClick(notification.id, notification.action_url)">
                                Толығырақ өту
                            </a>
                        </div>


                        <button @click="markAsRead(notification.id)"
                            :class="['mt-2 text-sm font-medium', notification.read ? 'text-gray-400 cursor-not-allowed' : 'text-blue-500 hover:underline']"
                            :disabled="notification.read">
                            {{ notification.read ? 'Оқылды' : 'Оқылды деп белгілеу' }}
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useToastStore } from '../stores/toast';
import { useNotificationStore } from '../stores/notification';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import 'dayjs/locale/kk';


dayjs.extend(relativeTime);
dayjs.locale('kk');

const notifications = ref([]);
const loading = ref(false);
const toastStore = useToastStore();
const notificationStore = useNotificationStore();

const fetchNotifications = async () => {
    loading.value = true;
    try {
        const response = await axios.get('/api/notifications/');
        notifications.value = response.data.map(notification => ({
            ...notification,
            read: notification.is_read,
            timestamp: notification.timestamp,
        }));
        console.log('Уведомления:', notifications.value);
    } catch (error) {
        console.error('Ошибка при загрузке уведомлений:', error);
        toastStore.showToast('Не удалось загрузить уведомления.');
    } finally {
        loading.value = false;
    }
};

const markAsRead = async (notifId) => {
    try {
        await axios.post(`/api/notifications/${notifId}/read/`);
        const notification = notifications.value.find(n => n.id === notifId);
        if (notification && !notification.read) {
            notification.read = true;
            notificationStore.decrementUnreadCount();
            toastStore.showToast(3000, 'Хабарлама оқылды деп белгіленді.', 'bg-emerald-500');
        }
    } catch (error) {
        console.error('Ошибка при обновлении уведомления:', error);
        toastStore.showToast(3000, 'Хабарламаны жаңарту мүмкін болмады.', 'bg-red-500');
    }
};

const handleClick = (notifId, actionUrl) => {
    markAsRead(notifId);
    window.location.href = actionUrl;
};

const formatTime = (timestamp) => {
    return dayjs(timestamp).fromNow();
};

onMounted(() => {
    fetchNotifications();
});
</script>

<style scoped>
.transition {
    transition: all 0.3s ease;
}

button:hover {
    transform: translateX(2px);
}

button:disabled {
    cursor: not-allowed;
    opacity: 0.5;
}
</style>
