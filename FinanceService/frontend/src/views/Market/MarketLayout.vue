<template>
  <div class="min-h-screen bg-slate-50 pt-28 pb-20 font-pretendard">
    <div class="max-w-6xl mx-auto px-6">
      <nav class="flex gap-8 border-b border-slate-200 mb-10 overflow-x-auto whitespace-nowrap scrollbar-hide">
        <router-link 
          v-for="menu in marketMenus" :key="menu.name"
          :to="{ name: menu.routeName }"
          class="pb-4 text-sm font-bold transition-all relative"
          active-class="text-blue-600 after:absolute after:bottom-0 after:left-0 after:w-full after:h-0.5 after:bg-blue-600"
        >
          {{ menu.name }}
        </router-link>
      </nav>

      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup>
const marketMenus = [
  { name: '시장 대시보드', routeName: 'market-overview' },
  { name: '실시간 환율', routeName: 'market-exchange' },
  { name: '원자재 시세', routeName: 'market-commodity' }
]
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>