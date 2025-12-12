<script setup>
import { RouterView } from 'vue-router'
// 분리한 컴포넌트들을 불러옵니다.
import TheHeader from '@/components/layout/TheHeader.vue'
import TheFooter from '@/components/layout/TheFooter.vue'
</script>

<template>
  <TheHeader />

  <main class="container mx-auto px-4 py-8 min-h-screen bg-gray-50">
    <RouterView />
  </main>

  <TheFooter />
</template>

<style scoped>
</style>