<script setup>
import { computed } from 'vue'

const props = defineProps({
  news: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

// 🐜 날짜 형식을 "2025.12.23 15:00" 포맷으로 변환하는 함수
const formatFullDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  
  const yyyy = date.getFullYear()
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  const dd = String(date.getDate()).padStart(2, '0')
  const hh = String(date.getHours()).padStart(2, '0')
  const min = String(date.getMinutes()).padStart(2, '0')
  
  return `${yyyy}.${mm}.${dd} ${hh}:${min}`
}
</script>

<template>
  <div class="w-full">
    <div v-if="isLoading" class="space-y-6">
      <div v-for="i in 4" :key="i" class="animate-pulse flex flex-col gap-3">
        <div class="h-5 bg-slate-100 rounded-lg w-full"></div>
        <div class="h-3 bg-slate-50 rounded-md w-1/3"></div>
      </div>
    </div>

    <ul v-else class="divide-y divide-slate-50">
      <li v-for="(item, index) in news" :key="index" class="group">
        <a :href="item.link" target="_blank" 
           class="flex flex-col gap-3 py-6 px-3 transition-all duration-300 group-hover:bg-slate-50/80 rounded-3xl">
          
          <h4 class="text-base md:text-[17px] font-bold text-slate-800 leading-snug tracking-tight group-hover:text-blue-600 transition-colors line-clamp-2">
            {{ item.title }}
          </h4>
          
          <div class="flex items-center gap-3">
            <span class="text-[12px] font-medium text-slate-400 tabular-nums">
              {{ formatFullDate(item.pubDate) }}
            </span>
            
            <span class="w-px h-2 bg-slate-200"></span>
            
            <span class="text-[12px] font-bold text-blue-500/70 uppercase tracking-tight">
              Finance Insight
            </span>
          </div>
        </a>
      </li>

      <div v-if="news.length === 0 && !isLoading" class="py-16 text-center">
        <p class="text-sm text-slate-400 font-medium italic">현재 새로운 소식이 없습니다. 🐜</p>
      </div>
    </ul>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>