<script setup>
import { ref, onMounted, computed } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import PageHeader from '@/components/common/PageHeader.vue' 
import NewsList from '@/components/news/NewsList.vue'

const financeStore = useFinanceStore()

// 검색 상태 관리
const searchQuery = ref('')
const activeCategory = ref('general')

// 카테고리 목록 (value는 백엔드로 보낼 값)
const categories = [
  { label: '전체', value: 'general' },
  { label: '📈 증시', value: 'stock' },
  { label: '💻 IT/테크', value: 'tech' },     // 추가됨
  { label: '💰 코인', value: 'crypto' },
  { label: '📊 경제/금리', value: 'economy' }, // 추가됨
  { label: '🏡 부동산', value: 'realestate' },
  { label: '🇺🇸 해외증시', value: 'global' },
  { label: '🆕 공모주', value: 'ipo' },       // 추가됨
]
onMounted(() => {
  // 데이터가 없으면 기본값으로 호출
  if (financeStore.news.length === 0) {
    financeStore.fetchNews()
  }
})

// 🔍 검색 실행 함수
const handleSearch = () => {
  // 검색어가 있으면 카테고리는 무시하거나 초기화 가능 (여기선 검색어 우선)
  financeStore.fetchNews({
    query: searchQuery.value,
    category: activeCategory.value
  })
}

// 🏷 카테고리 변경 함수
const changeCategory = (catValue) => {
  activeCategory.value = catValue
  searchQuery.value = '' // 카테고리 누르면 검색어 초기화 (깔끔하게)
  financeStore.fetchNews({ category: catValue })
}

</script>

<template>
  <div class="min-h-screen bg-slate-50 font-pretendard">
    
    <PageHeader 
      title="Global News Feed" 
      subtitle="실시간 경제 이슈와 트렌드를 가장 빠르게 확인하세요."
      bgClass="bg-slate-900" 
    />

    <main class="max-w-4xl mx-auto px-6 -mt-8 relative z-20 pb-20">
      
      <div class="bg-white rounded-[2rem] p-6 shadow-lg shadow-slate-200/50 mb-8 border border-slate-100">
        
        <div class="relative flex items-center bg-slate-50 rounded-2xl border border-slate-200 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 transition-all mb-6">
          <span class="pl-4 text-slate-400">🔍</span>
          <input 
            v-model="searchQuery"
            @keyup.enter="handleSearch"
            type="text" 
            placeholder="관심있는 키워드를 검색해보세요 (예: 삼성전자, 금리)"
            class="w-full px-4 py-3.5 bg-transparent font-bold text-slate-700 placeholder:text-slate-400 focus:outline-none"
          />
          <button 
            @click="handleSearch"
            class="mr-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold text-sm transition-colors shadow-md shadow-blue-200"
          >
            검색
          </button>
        </div>

        <div class="flex flex-wrap gap-2">
          <button 
            v-for="cat in categories" 
            :key="cat.value"
            @click="changeCategory(cat.value)"
            class="px-4 py-2 rounded-full text-xs font-bold transition-all border"
            :class="activeCategory === cat.value 
              ? 'bg-slate-800 text-white border-slate-800 shadow-lg shadow-slate-300 transform scale-105' 
              : 'bg-white text-slate-500 border-slate-200 hover:border-slate-400 hover:text-slate-700 hover:bg-slate-50'"
          >
            {{ cat.label }}
          </button>
        </div>
      </div>

      <div class="bg-white rounded-[2rem] p-6 md:p-8 shadow-xl border border-slate-100 min-h-[400px]">
        <div class="flex items-center justify-between px-2 pb-6 border-b border-slate-50 mb-4">
          <div class="flex items-center gap-2">
            <span v-if="financeStore.isMainLoading" class="loading loading-spinner loading-xs text-blue-600"></span>
            <span v-else class="relative flex h-3 w-3">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
            </span>
            
            <h3 class="text-sm font-black text-slate-800">
              {{ searchQuery ? `'${searchQuery}' 검색 결과` : '실시간 뉴스 피드' }}
            </h3>
          </div>
          <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
            Update Live
          </span>
        </div>

        <NewsList 
          :news="financeStore.news" 
          :isLoading="financeStore.isMainLoading" 
        />
      </div>

    </main>
  </div>
</template>

<style scoped>
.font-pretendard { font-family: 'Pretendard', sans-serif; }
</style>