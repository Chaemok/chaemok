<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import PageHeader from '@/components/common/PageHeader.vue' 
import MarketTabs from '@/components/market/MarketTabs.vue'
import MarketIndexModal from '@/components/market/MarketIndexModal.vue' // 🐜 모달 임포트

const router = useRouter()
const stockSearch = ref('')
const marketIndices = ref({}) // 지수 데이터
const isLoading = ref(true)

// 모달 상태
const isIndexModalOpen = ref(false)
const selectedIndex = ref(null)

const onSearchStock = () => {
  if (!stockSearch.value) return
  router.push({ name: 'stock-detail', params: { code: stockSearch.value.toUpperCase() } })
}

// 지수 데이터 로드
const fetchMarketStatus = async () => {
  try {
    const res = await api.get('finlife/market-status/')
    marketIndices.value = res.data
  } catch (err) { console.error(err) } 
  finally { isLoading.value = false }
}

// 카드 클릭 시 모달 열기
const openIndexModal = (name, data) => {
  if (!data) return
  selectedIndex.value = { name, symbol: data.symbol }
  isIndexModalOpen.value = true
}

onMounted(fetchMarketStatus)
</script>

<template>
  <div>
    <PageHeader 
      title="Global Market Dashboard" 
      subtitle="전 세계 주요 지수와 금융 흐름을 한눈에 파악하세요."
      bgClass="bg-indigo-950" 
    />

    <div class="max-w-7xl mx-auto px-4 pb-20 -mt-8 relative z-20">
      <MarketTabs />

      <div class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        
        <div class="bg-gradient-to-br from-indigo-600 to-blue-700 rounded-[2.5rem] p-10 md:p-14 text-white shadow-xl shadow-indigo-200 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/4 blur-3xl"></div>
          
          <div class="relative z-10 max-w-2xl">
            <h2 class="text-3xl md:text-4xl font-black mb-4 tracking-tight">
              관심 있는 주식을 검색해보세요 🐜
            </h2>
            <p class="text-indigo-100 mb-8 font-medium text-lg">
              티커(Ticker) 또는 종목명을 입력하여 실시간 차트와 AI 분석 리포트를 확인하세요.
            </p>
            
            <div class="relative flex items-center">
              <input 
                v-model="stockSearch"
                @keyup.enter="onSearchStock"
                type="text" 
                placeholder="예: AAPL, TSLA, 삼성전자"
                class="w-full py-5 pl-8 pr-32 rounded-2xl bg-white text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-4 focus:ring-white/30 transition-all font-bold text-lg shadow-lg"
              />
              <button @click="onSearchStock" class="absolute right-2 top-2 bottom-2 bg-indigo-900 text-white px-6 rounded-xl font-black text-sm hover:bg-black transition-colors">
                검색
              </button>
            </div>
          </div>
        </div>

        <div>
          <h3 class="text-xl font-black text-slate-800 mb-4 px-2">🌏 주요 시장 지수</h3>
          <div v-if="isLoading" class="grid grid-cols-2 md:grid-cols-4 gap-4">
             <div v-for="n in 4" :key="n" class="h-32 bg-white rounded-3xl animate-pulse"></div>
          </div>
          <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <div 
              v-for="(data, name) in marketIndices" :key="name"
              @click="openIndexModal(name, data)"
              class="bg-white p-6 rounded-[2rem] shadow-sm border border-slate-100 hover:shadow-md hover:-translate-y-1 transition-all cursor-pointer group"
            >
              <div class="flex justify-between items-start mb-2">
                <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">{{ name }}</span>
                <span v-if="data" class="text-[10px] font-black px-2 py-1 rounded-full" 
                  :class="data.isUp ? 'bg-red-50 text-red-500' : 'bg-blue-50 text-blue-500'">
                  {{ data.rate }}
                </span>
              </div>
              <div v-if="data">
                <div class="text-2xl font-black text-slate-800">{{ data.value }}</div>
                <div class="text-xs font-bold mt-1" :class="data.isUp ? 'text-red-500' : 'text-blue-500'">
                  {{ data.isUp ? '▲' : '▼' }} {{ data.change }}
                </div>
              </div>
              <div v-else class="text-slate-300 text-sm font-bold mt-2">휴장 또는 데이터 없음</div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <MarketIndexModal 
      :is-open="isIndexModalOpen" 
      :index-info="selectedIndex" 
      @close="isIndexModalOpen = false" 
    />
  </div>
</template> 