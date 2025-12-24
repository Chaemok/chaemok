<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance'
// 분리한 컴포넌트 임포트
import ExchangeCalculator from '@/components/exchange/ExchangeCalculator.vue'
import ExchangeRateList from '@/components/exchange/ExchangeRateList.vue'
import ExchangeDetailModal from '@/components/exchange/ExchangeDetailModal.vue'

const store = useFinanceStore()
const exchangeRates = computed(() => store.exchangeRates || [])
const isLoading = ref(true)
const isModalOpen = ref(false)
const selectedCurrency = ref(null)

onMounted(async () => {
  isLoading.value = true
  // 스토어 함수 호출 (getExchangeRates 혹은 fetchExchangeRates)
  if (store.getExchangeRates) await store.getExchangeRates()
  else if (store.fetchExchangeRates) await store.fetchExchangeRates()
  isLoading.value = false
})

// 모달 열기 핸들러
const handleRateClick = (rateData) => {
  if (!rateData) return
  // 더미 과거 데이터 생성 (실제 API 연결 시 제거)
  const historicalData = getMockHistoricalData(rateData)
  selectedCurrency.value = { ...rateData, historicalData }
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
  selectedCurrency.value = null
}

// 더미 데이터 생성기 (안전한 파싱 적용)
const getMockHistoricalData = (rateData) => {
  const parse = (v) => parseFloat((v?.toString() || '0').replace(/,/g, ''))
  const baseVal = parse(rateData.kftc_deal_bas_r || rateData.deal_bas_r || '1000')
  
  const data = []
  const today = new Date()
  for (let i = 6; i >= 0; i--) {
    const d = new Date(today)
    d.setDate(today.getDate() - i)
    const mockRate = baseVal * (1 + (Math.random() * 0.04 - 0.02))
    data.push({ date: d.toISOString().split('T')[0], rate: mockRate.toFixed(2) })
  }
  return data.reverse()
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 pb-32 font-pretendard relative overflow-hidden">
    <div class="absolute top-0 right-0 -translate-y-1/4 translate-x-1/4 w-[600px] h-[600px] bg-blue-100/40 blur-[120px] rounded-full pointer-events-none z-0"></div>
    <div class="absolute bottom-0 left-0 translate-y-1/4 -translate-x-1/4 w-[500px] h-[500px] bg-indigo-50/60 blur-[100px] rounded-full pointer-events-none z-0"></div>

    <div class="max-w-4xl mx-auto px-6 pt-20 relative z-10">
      
      <div class="text-center mb-12 space-y-3">
        <h1 class="text-4xl font-black text-slate-900 tracking-tight leading-tight">
          오늘의 <span class="text-blue-600 inline-block relative">환율 계산기</span> 💰
        </h1>
        <p class="text-slate-500 text-lg font-medium">전 세계 통화의 실시간 환율을 확인하고 계산해보세요.</p>
      </div>

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-40">
        <div class="loading loading-spinner loading-lg text-blue-600"></div>
        <p class="mt-6 text-slate-400 font-bold animate-pulse">환율 정보를 불러오고 있어요...</p>
      </div>

      <div v-else class="space-y-10 animate-fade-in-up">
        
        <ExchangeCalculator :rates="exchangeRates" />

        <div class="space-y-4">
          <div class="flex items-center justify-between px-4">
            <h3 class="text-xl font-black text-slate-800">주요 통화 환율</h3>
            <span class="text-sm font-medium text-slate-400">매매기준율 기준</span>
          </div>
          
          <ExchangeRateList 
            :rates="exchangeRates" 
            @item-click="handleRateClick" 
          />
        </div>

      </div>
    </div>

    <ExchangeDetailModal
      :is-open="isModalOpen"
      :currency-data="selectedCurrency"
      @close="closeModal"
    />
  </div>
</template>

<style scoped>
.font-pretendard { font-family: 'Pretendard', sans-serif; }
.animate-fade-in-up { animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; transform: translateY(20px); }
@keyframes fadeInUp { to { opacity: 1; transform: translateY(0); } }
</style>