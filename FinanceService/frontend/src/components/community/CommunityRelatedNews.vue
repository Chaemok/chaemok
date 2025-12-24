<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '@/api'

// 🐜 뉴스 카테고리 정의
const categories = [
  { id: 'general', label: '📢 종합' },
  { id: 'stock', label: '📈 증권/주식' },
  { id: 'realestate', label: '🏠 부동산' },
  { id: 'crypto', label: '🪙 코인/토큰' },
  { id: 'global', label: '🇺🇸 해외증시' },
]

const currentCategory = ref('general')
const newsList = ref([])
const isLoading = ref(false)

// 뉴스 가져오기 함수
const fetchNews = async () => {
  isLoading.value = true
  newsList.value = [] // 깜빡임 효과 (로딩감)
  try {
    const res = await api.get('finlife/news/', {
      params: { category: currentCategory.value }
    })
    newsList.value = res.data
  } catch (err) {
    console.error('뉴스 로드 실패')
  } finally {
    isLoading.value = false
  }
}

// 탭이 바뀌면 뉴스 다시 불러오기
watch(currentCategory, () => {
  fetchNews()
})

// 처음 켜지면 실행
onMounted(fetchNews)
</script>

<template>
  <div class="mt-8 bg-white rounded-[2rem] border border-slate-100 shadow-lg shadow-slate-200/50 p-6 md:p-8">
    
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-6">
      <div class="space-y-1">
        <h3 class="text-xl font-black text-slate-800 flex items-center gap-2">
          📰 오늘의 금융 브리핑
          <span class="text-[10px] bg-red-50 text-red-600 px-2 py-0.5 rounded-md uppercase tracking-wider animate-pulse">Live</span>
        </h3>
        <p class="text-xs text-slate-400 font-bold">실시간 주요 금융 뉴스를 확인하고 투자 아이디어를 얻으세요.</p>
      </div>

      <div class="flex gap-2 overflow-x-auto no-scrollbar pb-2 md:pb-0">
        <button 
          v-for="cat in categories" :key="cat.id"
          @click="currentCategory = cat.id"
          class="px-4 py-2 rounded-xl text-xs font-black transition-all whitespace-nowrap border"
          :class="currentCategory === cat.id 
            ? 'bg-blue-900 text-white border-blue-900 shadow-md transform scale-105' 
            : 'bg-slate-50 text-slate-400 border-slate-100 hover:bg-slate-100 hover:text-slate-600'"
        >
          {{ cat.label }}
        </button>
      </div>
    </div>

    <div class="relative min-h-[200px]">
      
      <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-white/80 z-10">
        <span class="loading loading-dots loading-lg text-blue-900"></span>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <a v-for="(news, idx) in newsList" :key="idx" :href="news.link" target="_blank"
           class="group flex flex-col justify-between p-5 bg-slate-50 border border-slate-100 rounded-2xl hover:bg-white hover:border-blue-200 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
          
          <div class="space-y-2">
            <h4 class="text-sm font-bold text-slate-800 group-hover:text-blue-600 leading-snug line-clamp-2" v-html="news.title"></h4>
            <p class="text-xs text-slate-500 line-clamp-2 leading-relaxed opacity-80" v-html="news.description"></p>
          </div>
          
          <div class="flex items-center justify-between mt-4 border-t border-slate-200/50 pt-3">
            <span class="text-[10px] font-bold text-slate-400">{{ news.pubDate }}</span>
            <span class="text-[10px] font-black text-blue-400 group-hover:translate-x-1 transition-transform">Read More →</span>
          </div>
        </a>
      </div>
      
    </div>
  </div>
</template>

<style scoped>
/* 횡스크롤바 숨기기 */
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>