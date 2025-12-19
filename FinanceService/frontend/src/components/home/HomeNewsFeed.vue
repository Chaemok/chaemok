<script setup>
import { useFinanceStore } from '@/stores/finance'
const store = useFinanceStore()
</script>

<template>
  <div class="card bg-white shadow-sm border border-slate-100 rounded-[2rem] p-8">
    <h3 class="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
      🗞️ 금융 헤드라인
    </h3>
    
    <div class="space-y-6">
      <div v-if="store.isLoading" v-for="n in 3" :key="n" class="space-y-2">
        <div class="h-4 w-3/4 bg-slate-100 animate-pulse rounded"></div>
        <div class="h-3 w-full bg-slate-100 animate-pulse rounded"></div>
      </div>

      <a v-else v-for="item in store.news" :key="item.link" :href="item.link" target="_blank" 
         class="group block space-y-2 hover:bg-slate-50 p-2 rounded-xl transition-all">
        <h4 class="font-bold text-slate-700 group-hover:text-emerald-600 line-clamp-1 transition-colors" v-html="item.title"></h4>
        <p class="text-xs text-slate-400 line-clamp-2 leading-relaxed" v-html="item.description"></p>
        <div class="text-[10px] text-slate-300">{{ item.pubDate }}</div>
      </a>
    </div>
  </div>
</template>