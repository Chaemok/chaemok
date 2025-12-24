<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import NewsSearch from '@/components/news/NewsSearch.vue'
import NewsList from '@/components/news/NewsList.vue'

const financeStore = useFinanceStore()
const filterData = ref({ query: '', category: '전체' })

onMounted(async () => {
  if (financeStore.news.length === 0) {
    await financeStore.fetchQuickData()
  }
})

const handleSearch = (data) => {
  filterData.value = data
}

// 🐜 프론트엔드 필터링 로직 (검색어 + 카테고리)
const filteredNews = computed(() => {
  let list = financeStore.news
  
  if (filterData.value.category !== '전체') {
    list = list.filter(item => item.title.includes(filterData.value.category))
  }
  
  if (filterData.value.query) {
    list = list.filter(item => 
      item.title.toLowerCase().includes(filterData.value.query.toLowerCase())
    )
  }
  
  return list
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 pt-28 pb-20 font-pretendard">
    <div class="max-w-4xl mx-auto px-6">
      
      <div class="mb-12 text-center space-y-4">
        <h2 class="text-4xl font-black text-slate-900 tracking-tight">Smart News 📰</h2>
        <p class="text-slate-500 font-medium">실시간 금융 소식과 함께 똑똑한 투자 인사이트를 얻으세요.</p>
      </div>

      <div class="mb-12">
        <NewsSearch @search="handleSearch" />
      </div>

      <div class="bg-white rounded-[3.5rem] p-4 md:p-8 shadow-[0_30px_60px_rgba(0,0,0,0.05)] border border-white">
        <div class="flex items-center justify-between px-6 py-4 border-b border-slate-50 mb-4">
          <span class="text-sm font-black text-slate-800">최신 뉴스 {{ filteredNews.length }}건</span>
          <span class="text-[10px] font-bold text-slate-400 italic italic">Live Updates From Naver</span>
        </div>

        <NewsList 
          :news="filteredNews" 
          :isLoading="financeStore.isMainLoading" 
        />
      </div>
    </div>
  </div>
</template>