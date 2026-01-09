<script setup>
import PageHeader from '@/components/common/PageHeader.vue'
</script>

<template>
  <div class="min-h-screen bg-slate-100 font-pretendard">
    <PageHeader 
      title="Smart Ants Community" 
      subtitle="현명한 개미들의 투자 인사이트와 정보를 공유하세요."
      bgClass="bg-blue-900" 
    />

    <div class="max-w-5xl mx-auto px-4 pb-20 -mt-6 relative z-20">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<style scoped>
.font-pretendard { font-family: 'Pretendard', sans-serif; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>