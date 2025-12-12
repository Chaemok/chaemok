<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useFinanceStore } from '@/stores/finance'
import PageHeader from '@/components/layout/PageHeader.vue'

import ExchangeChart from '@/components/exchange/ExchangeChart.vue'
import ExchangeHistory from '@/components/exchange/ExchangeHistory.vue'
import ExchangeConverterModal from '@/components/exchange/ExchangeConverterModal.vue'

const store = useFinanceStore()
const rates = ref([])
const loading = ref(true)
const targetCurrency = ref('USD')
const isConverterOpen = ref(false)

// ✨ [핵심] 기간 상태를 부모가 관리 (기본값: 1개월)
const currentPeriod = ref('1mo') 

onMounted(async () => {
  try {
    const res = await axios.get(`${store.API_URL}/api/finances/exchange-rate/`)
    if (Array.isArray(res.data)) {
      rates.value = res.data.filter(r => r.cur_unit !== 'KRW')
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})

const changeCurrency = (currency) => {
  targetCurrency.value = currency
}
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-10 min-h-screen">
    
    <div class="flex flex-col md:flex-row justify-between items-end mb-8 gap-4">
      <PageHeader title="💱 환율 조회" subtitle="실시간 환율 정보와 차트를 한눈에 확인하세요." />
      
      <button 
        @click="isConverterOpen = true" 
        class="btn bg-gray-900 text-white hover:bg-blue-700 border-none shadow-lg rounded-full px-6 gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
        환율 계산기
      </button>
    </div>

    <div class="overflow-x-auto pb-2 mb-6 scrollbar-hide">
      <div class="tabs tabs-boxed bg-white p-1.5 rounded-2xl shadow-sm inline-flex border border-gray-100 min-w-max">
        <a v-for="c in ['USD', 'JPY(100)', 'EUR', 'CNY', 'GBP', 'AUD', 'CAD', 'HKD', 'SGD', 'NZD']" 
           :key="c"
           class="tab tab-lg rounded-xl transition-all font-bold px-6"
           :class="targetCurrency === c ? 'bg-gray-900 text-white shadow-md' : 'text-gray-500 hover:text-gray-900'"
           @click="changeCurrency(c)"
        >
          {{ c.replace('(100)', '') }}
        </a>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      <div class="lg:col-span-7 h-[600px]">
        <ExchangeChart 
          :currency="targetCurrency" 
          v-model:period="currentPeriod" 
        />
      </div>

      <div class="lg:col-span-5 h-[600px]">
        <ExchangeHistory 
          :currency="targetCurrency" 
          :period="currentPeriod" 
        />
      </div>
    </div>

    <ExchangeConverterModal 
      :is-open="isConverterOpen" 
      :rates="rates"
      :default-currency="targetCurrency"
      @close="isConverterOpen = false"
    />

  </div>
</template>

<style scoped>
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>