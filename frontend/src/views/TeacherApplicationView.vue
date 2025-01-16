<template>
    <div class="max-w-xl mx-auto bg-white p-8 mt-10 shadow rounded-lg">
        <h1 class="text-3xl font-bold mb-6 text-center text-gray-800">Оқытушыға өтінім</h1>

        <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded mb-4">
            {{ error }}
        </div>
        <div v-if="message" class="bg-green-100 text-green-700 p-4 rounded mb-4">
            {{ message }}
        </div>

        <div v-if="application && application.status !== 'rejected'" class="mb-6">
            <div class="mb-4">
                <span class="font-semibold text-gray-700">Өтініш мәртебесі: </span>
                <span :class="statusClass(application.status)" class="font-medium">
                    {{ translateStatus(application.status) }}
                </span>
            </div>
            <div class="mb-4">
                <span class="font-semibold text-gray-700">Жіберілген күн: </span>
                <span class="text-gray-600">
                    {{ application.submitted_at ? formatDate(application.submitted_at) : '---' }}
                </span>
            </div>
            <div class="mb-4">
                <span class="font-semibold text-gray-700">Тексерілді: </span>
                <span class="text-gray-600">
                    {{ application.reviewed_at ? formatDate(application.reviewed_at) : '---' }}
                </span>
            </div>
            <div class="mb-6">
                <span class="font-semibold text-gray-700">Құжаттар:</span>
                <ul class="list-disc list-inside">
                    <li v-for="doc in application.documents" :key="doc.id"
                        class="overflow-hidden text-ellipsis whitespace-nowrap w-64">
                        <a :href="doc.file" target="_blank" class="text-blue-600 hover:underline">
                            {{ getFileName(doc.file) }}
                        </a>
                    </li>
                </ul>
            </div>
            <div class="text-center">
                <RouterLink to="/"
                    class="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded shadow hover:bg-blue-700 transition-colors">
                    Басты бетке
                </RouterLink>
            </div>
        </div>

        <div v-else>
            <div v-if="application && application.status === 'rejected'" class="mb-6 text-center text-red-600">
                <p class="mb-2">
                    Сіздің алдыңғы өтінішіңіз қабылданбады.
                    <a href="#" @click.prevent="openModal" class="underline">Себебін көрсету.</a>
                </p>
                <p class="font-semibold text-gray-700">Өтініш мәртебесі:
                    <span :class="statusClass(application.status)">
                        {{ translateStatus(application.status) }}
                    </span>
                </p>
                <p class="font-semibold text-gray-700">Тексеру күні:
                    <span class="text-gray-600">
                        {{ application.reviewed_at ? formatDate(application.reviewed_at) : '1-3 жұмыс күнінде' }}
                    </span>
                </p>
            </div>

            <div v-if="isModalOpen" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="absolute inset-0 bg-black opacity-50" @click="closeModal"></div>

                <div
                    class="bg-white rounded-lg shadow-lg max-w-md w-full mx-4 p-6 relative overflow-y-auto max-h-[80vh]">
                    <button @click="closeModal" class="absolute top-2 right-2 text-gray-500 hover:text-gray-700">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>

                    <h2 class="text-xl font-bold mb-4 text-gray-800">Өтінімді қабылдамау себебі</h2>
                    <p class="text-gray-700 whitespace-pre-wrap">
                        {{ application.rejection_reason || 'Причина не указана.' }}
                    </p>
                </div>
            </div>

            <form @submit.prevent="submitForm" class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700">ТАӘ</label>
                    <input type="text" v-model="form.full_name" required
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2"
                        placeholder="Толық аты-жөніңізді енгізіңіз" />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700">Телефон</label>
                    <input type="tel" v-model="form.phone" required
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2"
                        placeholder="+7 (___) ___-__-__" />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700">Құжат</label>
                    <input type="file" ref="fileInput" required accept=".pdf,.jpg,.jpeg,.png" class="mt-1 block w-full text-sm text-gray-500
                           file:mr-4 file:py-2 file:px-4
                           file:rounded-md file:border-0
                           file:text-sm file:font-semibold
                           file:bg-blue-50 file:text-blue-700
                           hover:file:bg-blue-100" />
                </div>

                <button type="submit"
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                    Өтінімді жіберу
                </button>
            </form>
            <div class="text-center mt-4">
                <RouterLink to="/" class="  text-blue-600  hover:text-blue-800 transition-colors">
                    Басты бетке
                </RouterLink>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'

const application = ref(null)
const form = reactive({
    full_name: '',
    phone: '',
})
const error = ref('')
const message = ref('')
const fileInput = ref(null)

const isModalOpen = ref(false)

const openModal = () => {
    isModalOpen.value = true
}

const closeModal = () => {
    isModalOpen.value = false
}

const getApplication = () => {
    error.value = ''
    message.value = ''
    axios.get('/api/teacher-application/')
        .then(res => {
            application.value = res.data
            form.full_name = application.value.full_name || ''
            form.phone = application.value.phone || ''
        })
        .catch(err => {
            if (err.response && err.response.status === 404) {
                application.value = null
                message.value = 'Сіз әлі өтініш жіберген жоқсыз! Төмендегі форманы толтырыңыз.'
            } else {
                error.value = err.response?.data?.detail || 'Ошибка при получении заявки'
            }
        })
}

const submitForm = () => {
    error.value = ''
    message.value = ''

    const fd = new FormData()
    fd.append('full_name', form.full_name)
    fd.append('phone', form.phone)

    const file = fileInput.value?.files[0]
    if (!file) {
        error.value = 'Өтініш, құжатты жүктеңіз!'
        return
    }
    fd.append('document', file)

    axios.post('/api/teacher-application/', fd, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
        .then(res => {
            application.value = res.data
            message.value = 'Өтінім сәтті жіберілді және тексеруді күтуде.'
            form.full_name = ''
            form.phone = ''
            fileInput.value.value = null
        })
        .catch(err => {
            error.value = err.response?.data?.detail || 'Ошибка при отправке заявки'
        })
}

const formatDate = (dateString) => {
    const options = {
        year: 'numeric', month: 'long', day: 'numeric',
        hour: '2-digit', minute: '2-digit'
    }
    return new Date(dateString).toLocaleDateString(undefined, options)
}

const getFileName = (fileUrl) => {
    return decodeURIComponent(fileUrl.split('/').pop())
}

const translateStatus = (status) => {
    const statusMap = {
        'pending': 'Күтілуде',
        'approved': 'Расталды',
        'rejected': 'Қабылданбады',
    }
    return statusMap[status] || status
}

const statusClass = (status) => {
    const classes = {
        'pending': 'text-orange-500',
        'approved': 'text-green-500',
        'rejected': 'text-red-500',
    }
    return classes[status] || 'text-gray-500'
}

const logout = () => {
    axios.post('/api/logout/')
        .then(() => {
            window.location.href = '/login/'
        })
        .catch(err => {
            console.error('Ошибка при выходе:', err)
            error.value = 'Ошибка при выходе'
        })
}

const handleKeydown = (event) => {
    if (event.key === 'Escape' && isModalOpen.value) {
        closeModal()
    }
}

window.addEventListener('keydown', handleKeydown)

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeydown)
})

onMounted(() => {
    getApplication()
})
</script>

<style scoped>
.fixed {
    transition: opacity 0.3s ease;
}
</style>
