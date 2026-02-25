<template>
  <div class="grid grid-cols-4 gap-4 mb-10">
    <router-link v-for="menu in menus" :key="menu.name" :to="menu.path" 
      class="flex flex-col items-center gap-2 p-4 rounded-2xl hover:bg-indigo-50 transition-colors group">
      <div class="w-14 h-14 bg-white shadow-sm border border-slate-100 rounded-2xl flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
        {{ menu.icon }}
      </div>
      <span class="text-xs font-bold text-slate-600">{{ menu.name }}</span>
    </router-link>
  </div>
</template>

<script setup>
const menus = [
  { name: '주변 은행', icon: '📍', path: '/map' },
  { name: '환율 계산기', icon: '🧮', path: '/exchange' },
  // { name: 'AI 주식분석', icon: '🤖', path: '/stocks/recommend' },
  { name: '커뮤니티', icon: '💬', path: '/community' },
]
</script>