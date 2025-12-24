<script setup>
import TheNavbar from '@/components/layout/TheNavbar.vue' // 경로에 맞게 수정
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <TheNavbar />

    <main class="pt-[124px] max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
      <slot /> </main>
  </div>
</template>