<script setup>
import CommunityHeader from '@/components/community/CommunityHeader.vue'
</script>

<template>
  <div class="min-h-screen bg-slate-100 py-16 px-4">
    <div class="max-w-5xl mx-auto space-y-10">
      
      <CommunityHeader />

      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>

    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>