<script setup>
import { useToastStore } from '../stores/toast.js'
const store = useToastStore()


</script>

<template>

  <div v-if="store.isVisible"
    class="transition ease-in-out delay-500 duration-500 px-6 py-6 fixed top-full right-8 rounded-xl text-white shadow-xl"
    :class="store.classes">
    {{ store.message }}
  </div>
</template>


<style scoped></style>