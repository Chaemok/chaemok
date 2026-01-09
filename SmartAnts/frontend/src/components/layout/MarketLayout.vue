<script setup>
// PageHeader, Nav 제거 -> 각 페이지에서 개별 적용
</script>

<template>
  <div class="min-h-screen bg-slate-50 font-pretendard">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<style scoped>
.font-pretendard { font-family: 'Pretendard', sans-serif; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>