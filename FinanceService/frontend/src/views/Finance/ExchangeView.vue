<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance'
// 차트 컴포넌트 임포트
import ExchangeDetailModal from '@/components/exchange/ExchangeDetailModal.vue'

const store = useFinanceStore()
const exchangeRates = computed(() => store.exchangeRates)
const isLoading = ref(true)

// 모달 상태 관리
const isModalOpen = ref(false)
const selectedCurrencyForModal = ref(null)

onMounted(async () => {
  isLoading.value = true
  await store.getExchangeRates()
  isLoading.value = false
})

// --- 계산기 로직 (기존 유지) ---
const fromCurrency = ref('USD')
const toCurrency = ref('KRW')
const amount = ref(1)

const getRateToUSD = (currencyCode) => {
  if (currencyCode === 'USD') return 1
  const rateData = exchangeRates.value.find(rate => rate.cur_unit === currencyCode)
  if (!rateData) return null
  const kftcDealBasR = parseFloat(rateData.kftc_deal_bas_r.replace(/,/g, ''))
  if (currencyCode === 'KRW') return 1 / kftcDealBasR
  const usdRateData = exchangeRates.value.find(rate => rate.cur_unit === 'USD')
  const usdKftcDealBasR = parseFloat(usdRateData.kftc_deal_bas_r.replace(/,/g, ''))
  return usdKftcDealBasR / kftcDealBasR
}

const convertedAmount = computed(() => {
  const fromRate = getRateToUSD(fromCurrency.value)
  const toRate = getRateToUSD(toCurrency.value)
  if (!fromRate || !toRate) return 0
  return (amount.value * toRate / fromRate).toFixed(2)
})

const currencyOptions = computed(() => {
  const options = exchangeRates.value.map(rate => rate.cur_unit)
  if (!options.includes('KRW')) options.unshift('KRW')
  if (!options.includes('USD')) options.unshift('USD')
  return [...new Set(options)]
})

// --- 유틸리티 함수 ---
// 천단위 콤마
const formatNumber = (num) => {
  if (!num) return '0'
  return Number(num).toLocaleString(undefined, { maximumFractionDigits: 2 })
}

// 국기 이미지 URL 생성기 (flagcdn 사용)
const getFlagUrl = (currencyCode) => {
  if (!currencyCode) return ''
  let countryCode = currencyCode.substring(0, 2).toLowerCase()
  // 예외 처리
  if (currencyCode === 'EUR') countryCode = 'eu'
  if (currencyCode === 'KRW') countryCode = 'kr'
  if (currencyCode === 'JPY') countryCode = 'jp'
  if (currencyCode === 'CNH') countryCode = 'cn'

  return `https://flagcdn.com/w40/${countryCode}.png`
}

// --- 모달 관련 로직 ---
const openDetailModal = (rateData) => {
  // 🐜 실제 API에 과거 데이터가 없으므로, 현재 환율을 기준으로 그럴듯한 더미 과거 데이터를 생성합니다.
  const historicalData = getMockHistoricalData(rateData)
  selectedCurrencyForModal.value = { ...rateData, historicalData }
  isModalOpen.value = true
}

const closeDetailModal = () => {
  isModalOpen.value = false
  selectedCurrencyForModal.value = null
}

// 🐜 [더미 데이터 생성기] 실제 API 연결 시 이 부분을 제거하고 API 호출로 대체하세요.
const getMockHistoricalData = (currentRateData) => {
  const baseRate = parseFloat(currentRateData.kftc_deal_bas_r.replace(/,/g, ''))
  const data = []
  const today = new Date()
  
  for (let i = 6; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(today.getDate() - i)
    
    // -2% ~ +2% 사이의 랜덤 변동폭 생성
    const fluctuation = (Math.random() * 0.04 - 0.02)
    let mockRate = baseRate * (1 + fluctuation)
    if (i === 0) mockRate = baseRate // 오늘은 실제 데이터

    data.push({
      date: date.toISOString().split('T')[0],
      rate: mockRate.toFixed(2)
    })
  }
  return data.reverse() // 최신순 정렬
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 pb-32 font-pretendard relative overflow-hidden">
    
    <div class="absolute top-0 right-0 -translate-y-1/4 translate-x-1/4 w-[600px] h-[600px] bg-blue-100/40 blur-[120px] rounded-full pointer-events-none z-0"></div>
    <div class="absolute bottom-0 left-0 translate-y-1/4 -translate-x-1/4 w-[500px] h-[500px] bg-indigo-50/60 blur-[100px] rounded-full pointer-events-none z-0"></div>

    <div class="max-w-4xl mx-auto px-6 pt-20 relative z-10">
      
      <div class="text-center mb-12 space-y-3 animate-fade-in-up">
        <h1 class="text-4xl font-black text-slate-900 tracking-tight leading-tight">
          실시간 <span class="text-blue-600 inline-block relative">환율 계산기<svg class="absolute -bottom-2 left-0 w-full h-3 text-blue-200 -z-10 opacity-60" viewBox="0 0 100 10" preserveAspectRatio="none"><path d="M0 5 Q 50 10 100 5" stroke="currentColor" stroke-width="8" fill="none" /></svg></span> 💰
        </h1>
        <p class="text-slate-500 text-lg font-medium">전 세계 통화의 실시간 환율을 확인하고 계산해보세요.</p>
      </div>

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-40">
        <div class="loading loading-spinner loading-lg text-blue-600"></div>
        <p class="mt-6 text-slate-400 font-bold animate-pulse">환율 정보를 불러오고 있어요...</p>
      </div>

      <div v-else class="space-y-10 animate-fade-in-up" style="animation-delay: 0.1s;">
        
        <div class="bg-white rounded-[2.5rem] p-8 shadow-xl shadow-blue-500/5 border border-blue-50 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-64 h-64 bg-blue-50 rounded-full blur-3xl -z-10 translate-x-1/3 -translate-y-1/3 opacity-70"></div>
          
          <div class="flex flex-col md:flex-row gap-6 items-center justify-between relative z-10">
            <div class="flex-1 w-full space-y-2">
               <label class="text-sm font-bold text-slate-500 ml-2">보낼 때 (내가 가진 돈)</label>
               <div class="flex items-center bg-slate-50 p-2 rounded-2xl border border-slate-200 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-200 transition-all">
                <input type="number" v-model="amount" min="0" class="bg-transparent text-2xl font-black text-slate-800 p-3 focus:outline-none flex-1 text-right" placeholder="금액 입력" />
                 <select v-model="fromCurrency" class="bg-transparent text-lg font-bold text-blue-600 p-3 focus:outline-none cursor-pointer">
                  <option v-for="currency in currencyOptions" :key="currency" :value="currency">{{ currency }}</option>
                </select>
              </div>
            </div>

            <div class="shrink-0 flex items-center justify-center w-12 h-12 bg-blue-50 text-blue-600 rounded-full shadow-sm rotate-90 md:rotate-0 mt-4 md:mt-6">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>
             </div>

            <div class="flex-1 w-full space-y-2">
               <label class="text-sm font-bold text-slate-500 ml-2">받을 때 (예상 금액)</label>
               <div class="flex items-center bg-blue-600/5 p-2 rounded-2xl border border-blue-100">
                <input type="text" :value="formatNumber(convertedAmount)" readonly class="bg-transparent text-2xl font-black text-blue-600 p-3 focus:outline-none flex-1 text-right pointer-events-none" />
                 <select v-model="toCurrency" class="bg-transparent text-lg font-bold text-blue-700 p-3 focus:outline-none cursor-pointer">
                  <option v-for="currency in currencyOptions" :key="currency" :value="currency">{{ currency }}</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div class="space-y-4">
          <div class="flex items-center justify-between px-4">
            <h3 class="text-xl font-black text-slate-800">주요 통화 환율</h3>
            <span class="text-sm font-medium text-slate-400">매매기준율 기준</span>
          </div>

          <div class="bg-white rounded-[2rem] shadow-lg shadow-slate-200/50 border border-slate-100 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left">
                <thead class="bg-slate-50 border-b border-slate-100">
                  <tr>
                    <th class="py-4 px-6 text-sm font-black text-slate-500 uppercase tracking-wider">통화</th>
                    <th class="py-4 px-6 text-sm font-black text-slate-500 uppercase tracking-wider text-right">매매기준율</th>
                    <th class="py-4 px-6 text-sm font-black text-slate-500 uppercase tracking-wider text-right hidden md:table-cell">송금 보낼때</th>
                    <th class="py-4 px-6 text-sm font-black text-slate-500 uppercase tracking-wider text-right hidden md:table-cell">송금 받을때</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                  <tr v-for="rate in exchangeRates" :key="rate.cur_unit" 
                      @click="openDetailModal(rate)"
                      class="hover:bg-blue-50/50 transition-colors cursor-pointer group">
                    <td class="py-5 px-6">
                      <div class="flex items-center gap-4">
                        <img :src="getFlagUrl(rate.cur_unit)" alt="flag" class="w-8 h-8 rounded-full shadow-sm object-cover border border-slate-100 group-hover:scale-110 transition-transform" />
                        <div>
                          <div class="font-black text-slate-800 text-base">{{ rate.cur_unit }}</div>
                          <div class="text-xs font-bold text-slate-400 mt-0.5">{{ rate.cur_nm }}</div>
                        </div>
                      </div>
                    </td>
                    <td class="py-5 px-6 text-right">
                      <span class="font-black text-lg text-blue-600">{{ rate.kftc_deal_bas_r }}</span>
                    </td>
                    <td class="py-5 px-6 text-right hidden md:table-cell">
                      <span class="font-bold text-slate-600">{{ rate.tts }}</span>
                    </td>
                    <td class="py-5 px-6 text-right hidden md:table-cell">
                      <span class="font-bold text-slate-600">{{ rate.ttb }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <ExchangeDetailModal
      :is-open="isModalOpen"
      :currency-data="selectedCurrencyForModal"
      @close="closeDetailModal"
    />

  </div>
</template>

<style scoped>
.font-pretendard { font-family: 'Pretendard', sans-serif; }

/* 크롬 등에서 숫자 입력 화살표 제거 */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield; /* 파이어폭스 */
}

.animate-fade-in-up { animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; transform: translateY(20px); }
@keyframes fadeInUp {
  to { opacity: 1; transform: translateY(0); }
}
</style>