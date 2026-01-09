<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const menus = [
  { name: 'market-overview', label: '📊 시장 대시보드', activeClass: 'bg-indigo-600 text-white shadow-md' },
  { name: 'market-exchange', label: '💱 오늘의 환율', activeClass: 'bg-blue-600 text-white shadow-md' },
  { name: 'market-commodity', label: '🪙 금/은 시세', activeClass: 'bg-yellow-500 text-white shadow-md' }
]
</script>

<template>
  <nav class="flex flex-wrap gap-2 mb-8 bg-white/90 backdrop-blur-md p-2 rounded-2xl shadow-lg shadow-slate-200/50 border border-white mx-auto max-w-fit relative z-30">
    <router-link 
      v-for="menu in menus" :key="menu.name"
      :to="{ name: menu.name }"
      class="px-6 py-3 rounded-xl font-black text-sm transition-all flex items-center gap-2"
      :class="route.name === menu.name ? menu.activeClass : 'text-slate-500 hover:bg-slate-100 hover:text-slate-900'"
    >
      {{ menu.label }}
    </router-link>
  </nav>
</template>