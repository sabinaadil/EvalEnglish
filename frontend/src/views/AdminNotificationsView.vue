<template>
    <div class="max-w-screen-lg mx-auto my-6 p-6 bg-white shadow rounded-lg">
        <h1 class="text-2xl font-bold mb-6 text-center text-gray-800">Оқытушыға өтінімдер</h1>

        <transition name="fade">
            <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded mb-4">
                {{ error }}
            </div>
        </transition>

        <div class="mb-6">
            <div class="relative">
                <input type="text" v-model="searchTerm" placeholder="ФИО бойынша іздеу..."
                    class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 transition duration-200" />
                <svg xmlns="http://www.w3.org/2000/svg"
                    class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1111.25 4.5a7.5 7.5 0 016.4 12.15z" />
                </svg>
            </div>
        </div>

        <div v-if="filteredApplications.length === 0 && !error">
            <p class="text-gray-600 text-center"><strong>Күтілуде</strong> немесе іздеу нәтижелері жоқ.</p>
        </div>
        <div v-else class="grid grid-cols-1 gap-6">
            <div v-for="app in paginatedApplications" :key="app.id"
                class="p-6 border rounded-lg shadow-sm bg-gray-50 flex flex-col justify-between transition duration-300 hover:bg-gray-100">
                <div>
                    <p class="font-semibold text-lg text-gray-700">{{ app.full_name || '—' }}</p>
                    <p class="text-gray-600">Пошта: {{ app.user_email }}</p>
                    <p class="text-gray-600">Телефон: {{ app.phone || '—' }}</p>
                    <p class="text-gray-600">Жіберілген күн: {{ app.submitted_at ? formatDate(app.submitted_at) : '---'
                        }}</p>
                </div>
                <div class="mt-4">
                    <span class="font-semibold text-gray-700">Құжат:</span>
                    <ul class="list-disc list-inside mt-2">
                        <li v-for="doc in app.documents" :key="doc.id" class="text-blue-600 hover:underline">
                            <a :href="doc.file" target="_blank">{{ getFileName(doc.file) }}</a>
                        </li>
                    </ul>
                </div>

                <div class="mt-6 flex justify-end space-x-3">
                    <button
                        class="flex items-center px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
                        @click="approveApplication(app.id)">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                        Мақұлдау
                    </button>
                    <button
                        class="flex items-center px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
                        @click="openRejectModal(app.id)">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                        </svg>
                        Бас тарту
                    </button>
                </div>
            </div>
        </div>

        <div v-if="totalPages > 1" class="mt-6 flex justify-center items-center space-x-2">
            <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1"
                class="px-3 py-1 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
                Алдыңғы
            </button>
            <button v-for="page in paginationRange" :key="page" @click="changePage(page)" :class="[
                'px-4 py-1 rounded transition-colors',
                page === currentPage ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            ]">
                {{ page }}
            </button>
            <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages"
                class="px-3 py-1 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
                Келесі
            </button>
        </div>

        <transition name="modal">
            <div v-if="showRejectModal" class="fixed inset-0 flex items-center justify-center z-50">
                <div class="absolute inset-0 bg-black opacity-50" @click="closeRejectModal"></div>

                <div
                    class="bg-white rounded-lg shadow-lg max-w-md w-full mx-4 p-6 relative overflow-y-auto max-h-[80vh]">
                    <button @click="closeRejectModal" class="absolute top-2 right-2 text-gray-500 hover:text-gray-700">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>

                    <h2 class="text-xl font-bold mb-4 text-gray-800">Өтінімді қабылдамау себебі</h2>

                    <div class="mb-4">
                        <span class="block text-gray-700 mb-2">Себебін таңдаңыз:</span>
                        <div class="flex flex-wrap gap-2">
                            <button v-for="reason in predefinedReasons" :key="reason"
                                @click="selectPredefinedReason(reason)"
                                class="px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors">
                                {{ reason }}
                            </button>
                        </div>
                    </div>

                    <div>
                        <textarea v-model="rejectReason" rows="4"
                            class="w-full border rounded p-2 focus:border-blue-500 focus:ring-blue-500"
                            placeholder="Егер ұсынылған себептердің ешқайсысы сәйкес келмесе, себебіңізді осында енгізіңіз..."></textarea>
                    </div>

                    <div class="flex justify-end space-x-3 mt-6">
                        <button @click="closeRejectModal"
                            class="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400 transition-colors">
                            Болдырмау
                        </button>
                        <button @click="rejectApplication(selectedAppId)"
                            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors">
                            Бас тарту
                        </button>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'

const applications = ref([])
const error = ref('')

const currentPage = ref(1)
const itemsPerPage = 2
const totalPages = computed(() => Math.ceil(filteredApplications.value.length / itemsPerPage))

const searchTerm = ref('')

const showRejectModal = ref(false)
const rejectReason = ref('')
const selectedAppId = ref(null)

const predefinedReasons = [
    'Біліктілік жеткіліксіз',
    'Өтінімдегі дұрыс емес ақпарат',
    'Талаптарға сәйкессіздік',
    'Басқа себептер'
]

function openRejectModal(applicationId) {
    selectedAppId.value = applicationId
    rejectReason.value = ''
    showRejectModal.value = true
}

function closeRejectModal() {
    showRejectModal.value = false
    rejectReason.value = ''
    selectedAppId.value = null
}

function selectPredefinedReason(reason) {
    rejectReason.value = reason
}

function fetchPendingApplications() {
    error.value = ''
    axios.get('/api/teacher-applications/pending_list/')
        .then(res => {
            applications.value = res.data
        })
        .catch(err => {
            error.value = err.response?.data?.detail || 'Ошибка при загрузке заявок'
        })
}

function approveApplication(applicationId) {
    axios.post(`/api/teacher-applications/${applicationId}/approve/`)
        .then(() => {
            applications.value = applications.value.filter(a => a.id !== applicationId)
        })
        .catch(err => {
            error.value = err.response?.data?.detail || 'Ошибка при одобрении заявки'
        })
}

function rejectApplication(applicationId) {
    if (!rejectReason.value.trim()) {
        error.value = 'Қабылдамау себебін көрсетіңіз.'
        return
    }

    axios.post(`/api/teacher-applications/${applicationId}/reject/`, { reason: rejectReason.value })
        .then(() => {
            applications.value = applications.value.filter(a => a.id !== applicationId)
            closeRejectModal()
        })
        .catch(err => {
            error.value = err.response?.data?.detail || 'Ошибка при отклонении заявки'
        })
}

function getFileName(fileUrl) {
    return decodeURIComponent(fileUrl.split('/').pop())
}

function formatDate(dateString) {
    const options = {
        year: 'numeric', month: 'long', day: 'numeric',
        hour: '2-digit', minute: '2-digit'
    }
    return new Date(dateString).toLocaleDateString(undefined, options)
}

const filteredApplications = computed(() => {
    if (!searchTerm.value) {
        return applications.value
    }
    return applications.value.filter(app =>
        app.full_name.toLowerCase().includes(searchTerm.value.toLowerCase())
    )
})

const paginatedApplications = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage
    const end = start + itemsPerPage
    return filteredApplications.value.slice(start, end)
})

const paginationRange = computed(() => {
    const range = []
    for (let i = 1; i <= totalPages.value; i++) {
        range.push(i)
    }
    return range
})

function changePage(page) {
    if (page < 1) page = 1
    if (page > totalPages.value) page = totalPages.value
    currentPage.value = page
}

watch(searchTerm, () => {
    currentPage.value = 1
})

import { onUnmounted, watch } from 'vue'

function handleKeydown(event) {
    if (event.key === 'Escape' && showRejectModal.value) {
        closeRejectModal()
    }
}

window.addEventListener('keydown', handleKeydown)

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeydown)
})

onMounted(() => {
    fetchPendingApplications()
})
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
    transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
    transform: scale(0.95);
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.pagination {
    display: flex;
    justify-content: center;
    margin-top: 1rem;
}

.pagination button {
    margin: 0 0.25rem;
}
</style>
