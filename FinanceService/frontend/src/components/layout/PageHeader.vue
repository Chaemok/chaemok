<script setup>
defineProps({
  title: String,
  subtitle: String
})
</script>

<template>
  <div class="mb-8">
    <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ title }}</h1>
    <p v-if="subtitle" class="text-gray-500">{{ subtitle }}</p>
  </div>
</template>