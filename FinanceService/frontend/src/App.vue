<script setup>
import { RouterView } from 'vue-router'
import TheNavbar from '@/components/common/TheNavbar.vue'
import TheFooter from '@/components/layout/TheFooter.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col font-sans">
    <TheNavbar />

    <main class="flex-1">
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" :key="$route.fullPath" />
        </transition>
      </RouterView>
    </main>

    <TheFooter />
  </div>
</template>
<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>