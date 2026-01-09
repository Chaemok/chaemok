<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import api from '@/api'
import PageHeader from '@/components/common/PageHeader.vue' // 🐜
import MarketTabs from '@/components/market/MarketTabs.vue' // 🐜
import ExchangeCalculator from '@/components/exchange/ExchangeCalculator.vue'
import ExchangeRateList from '@/components/exchange/ExchangeRateList.vue'
import ExchangeDetailModal from '@/components/exchange/ExchangeDetailModal.vue'

const store = useFinanceStore()
const localExchangeRates = ref([])
const isLoading = ref(true)
const isModalOpen = ref(false)
const selectedCurrency = ref(null)

const displayRates = computed(() => {
  if (store.exchangeRates && store.exchangeRates.length > 0) return store.exchangeRates
  return localExchangeRates.value
})

onMounted(async () => {
  isLoading.value = true
  try {
    if (store.fetchExchangeRates) await store.fetchExchangeRates()
    if (!store.exchangeRates || store.exchangeRates.length === 0) {
      const res = await api.get('finlife/exchange-rate/') // URL 수정: views.py에 맞춤
      localExchangeRates.value = res.data
    }
  } catch (err) { console.error(err) } 
  finally { isLoading.value = false }
})

const handleRateClick = (rateData) => {
  if (!rateData) return
  selectedCurrency.value = rateData
  isModalOpen.value = true
}
</script>

<template>
  <div>
    <PageHeader 
      title="Exchange Rates Today" 
      subtitle="실시간 환율 정보를 확인하고 간편하게 계산해보세요."
      bgClass="bg-blue-900" 
    />

    <div class="max-w-7xl mx-auto px-4 pb-20 -mt-8 relative z-20">
      <MarketTabs />

      <div class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div v-if="isLoading" class="flex flex-col items-center justify-center py-40">
          <span class="loading loading-spinner loading-lg text-blue-600"></span>
          <p class="mt-6 text-slate-400 font-bold animate-pulse">환율 정보를 불러오고 있습니다... 🐜</p>
        </div>

        <div v-else-if="!displayRates || displayRates.length === 0" class="flex flex-col items-center justify-center py-40 bg-white rounded-[3rem] border border-slate-100 shadow-sm text-center px-4">
          <span class="text-5xl mb-6">🏦</span>
          <h3 class="text-xl font-black text-slate-800 mb-2">현재 환율 정보를 불러올 수 없습니다.</h3>
          <p class="text-slate-500 font-medium">공휴일이나 비영업 시간에는 데이터가 제공되지 않을 수 있습니다.</p>
        </div>

        <div v-else class="space-y-10">
          <div class="bg-white rounded-[2.5rem] shadow-xl shadow-slate-200/50 p-8 border border-white">
            <ExchangeCalculator :rates="displayRates" />
          </div>
          <div class="space-y-4">
            <div class="flex items-center justify-between px-4">
              <h3 class="text-xl font-black text-slate-800">💱 주요 통화 환율</h3>
              <span class="text-xs font-bold text-slate-400 bg-slate-100 px-3 py-1 rounded-full">매매기준율 기준</span>
            </div>
            <ExchangeRateList :rates="displayRates" @item-click="handleRateClick" />
          </div>
        </div>

        <ExchangeDetailModal :is-open="isModalOpen" :currency-data="selectedCurrency" @close="isModalOpen = false"/>
      </div>
    </div>
  </div>
</template>