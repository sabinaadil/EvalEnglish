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
                <div class="space-y-2 mt-2">
                    <div v-for="doc in application.documents" :key="doc.id"
                        class="flex items-center justify-between bg-gray-50 border border-gray-300 rounded-md p-2 shadow-sm">
                        <div class="flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600 mr-3" fill="none"
                                viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zM14 3v5h5M10 12h4m-4 4h4" />
                            </svg>
                            <a :href="doc.file" target="_blank"
                                class="text-sm text-gray-700 truncate w-52 hover:underline">
                                {{ getFileName(doc.file) }}
                            </a>
                        </div>
                        <button type="button" class="text-green-600 hover:text-green-800 focus:outline-none">
                            <a :href="doc.file" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                    viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                </svg></a>

                        </button>
                    </div>
                </div>
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
                    <input type="file" ref="fileInput" multiple required accept=".pdf,.jpg,.jpeg,.png"
                        @change="handleFileChange" class="mt-1 block w-full text-sm text-gray-500
                           file:mr-4 file:py-2 file:px-4
                           file:rounded-md file:border-0
                           file:text-sm file:font-semibold
                           file:bg-blue-50 file:text-blue-700
                           hover:file:bg-blue-100" />
                </div>
                <div v-if="files.length" class="mt-4">
                    <p class="text-sm font-medium text-gray-700 mb-2">Таңдалған құжаттар:</p>
                    <div class="space-y-2">
                        <div v-for="(file, index) in files" :key="index"
                            class="flex items-center justify-between bg-gray-50 border border-gray-300 rounded-md p-2 shadow-sm">
                            <div class="flex items-center">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600 mr-3" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zM14 3v5h5M10 12h4m-4 4h4" />
                                </svg>
                                <span class="text-sm text-gray-700 truncate w-52">{{ file.name }}</span>
                            </div>
                            <button type="button" @click="removeFile(index)"
                                class="text-red-600 hover:text-red-800 focus:outline-none">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                                    stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>
                    </div>
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
import { useUserStore } from '../stores/user'
import axios from 'axios'
import { RouterLink } from 'vue-router'


const userStore = useUserStore()
const application = ref(null)
const form = reactive({
    full_name: '',
    phone: '',
    documents: [],
})

const error = ref('')
const message = ref('')
const fileInput = ref(null)
const files = ref([]);

const isModalOpen = ref(false)

const openModal = () => {
    isModalOpen.value = true
}

const closeModal = () => {
    isModalOpen.value = false
}

const removeFile = (index) => {
    files.value.splice(index, 1);
};

const getApplication = () => {
    if (userStore.user.role !== 'teacher') {
        message.value = 'Тек оқытушылар өтінім жіберуге құқылы.';
        return;
    }
    error.value = '';
    message.value = '';
    axios.get('/api/teacher-application/')
        .then(res => {
            application.value = res.data;
            form.full_name = application.value.full_name || '';
            form.phone = application.value.phone || '';
        })
        .catch(err => {
            if (err.response && err.response.status === 404) {
                application.value = null;
                message.value = 'Сіз әлі өтініш жіберген жоқсыз! Төмендегі форманы толтырыңыз.';
            } else {
                error.value = err.response?.data?.detail || 'Ошибка при получении заявки';
            }
        });
};


const handleFileChange = () => {
    const selectedFiles = fileInput.value?.files;
    if (selectedFiles) {
        files.value = [...files.value, ...Array.from(selectedFiles)];
    }
};

const submitForm = () => {
    if (userStore.user.role !== 'teacher') {
        message.value = 'Тек оқытушылар өтінім жіберуге құқылы.';
        return;
    }
    error.value = '';
    message.value = '';

    const fd = new FormData();
    fd.append('full_name', form.full_name);
    fd.append('phone', form.phone);

    if (files.value.length === 0) {
        error.value = 'Өтініш, кемінде бір құжатты жүктеңіз!';
        return;
    }

    files.value.forEach((file, index) => {
        fd.append(`documents`, file);
    });

    axios.post('/api/teacher-application/', fd, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
        .then((res) => {
            application.value = res.data;
            message.value = 'Өтінім сәтті жіберілді және тексеруді күтуде.';
            form.full_name = '';
            form.phone = '';
            files.value = [];
            fileInput.value.value = null;
        })
        .catch((err) => {
            error.value = err.response?.data?.detail || 'Ошибка при отправке заявки';
        });
};


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
    if (userStore.user.role === 'teacher') {
        getApplication()
    }

})
</script>

<style scoped>
.fixed {
    transition: opacity 0.3s ease;
}
</style>
