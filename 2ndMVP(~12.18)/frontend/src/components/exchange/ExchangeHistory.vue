<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'
import { useFinanceStore } from '@/stores/finance'

const store = useFinanceStore()
const props = defineProps({
  currency: { type: String, required: true },
  period: { type: String, required: true }
})

const historyList = ref([])
const loading = ref(false)

// ✨ 통화 기호 매핑 함수
const getSymbol = (code) => {
  const symbols = {
    'USD': '$', 'JPY(100)': '¥', 'EUR': '€', 'CNY': '¥', 'GBP': '£',
    'AUD': 'A$', 'CAD': 'C$', 'HKD': 'HK$', 'SGD': 'S$', 'NZD': 'NZ$', 'KRW': '₩'
  }
  return symbols[code] || ''
}

const fetchHistory = async () => {
  loading.value = true
  try {
    const res = await axios.get(`${store.API_URL}/api/finances/exchange-rate/chart-data/`, {
      params: { symbol: props.currency, period: props.period }
    })
    
    const prices = res.data.data
    const dates = res.data.labels
    const list = []

    if (prices.length > 0) {
      for (let i = prices.length - 1; i >= 0; i--) {
        const current = prices[i]
        const prev = i > 0 ? prices[i - 1] : current
        const diff = current - prev
        
        list.push({
          date: dates[i],
          price: Number(current).toLocaleString(undefined, { maximumFractionDigits: 2 }),
          diff: Number(Math.abs(diff)).toLocaleString(undefined, { maximumFractionDigits: 2 }),
          status: diff > 0 ? '상승' : (diff < 0 ? '하락' : '보합')
        })
      }
    }
    historyList.value = list

  } catch (e) {
    console.error("히스토리 로딩 실패", e)
    historyList.value = []
  } finally {
    loading.value = false
  }
}

onMounted(fetchHistory)
watch([() => props.currency, () => props.period], fetchHistory)
</script>

<template>
  <div class="bg-white shadow-xl border border-gray-100 rounded-[2rem] overflow-hidden h-full flex flex-col">
    <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
       <h3 class="font-bold text-gray-800 flex items-center gap-2">
         📅 일자별 환율
         <span class="text-sm font-normal text-gray-500">
           ({{ currency.replace('(100)', '') }} {{ getSymbol(currency) }})
         </span>
       </h3>
       <span class="badge badge-ghost text-xs text-gray-500">{{ props.period === '1w' ? '최근 1주' : props.period === '1y' ? '최근 1년' : `최근 ${props.period.replace('mo', '개월')}` }}</span>
    </div>
    
    <div class="overflow-x-auto flex-1 custom-scrollbar min-h-[300px]">
      <table class="table table-pin-rows w-full">
        <thead>
          <tr class="bg-white text-gray-500 text-xs border-b border-gray-100">
            <th class="bg-gray-50/80">날짜</th>
            <th class="text-right bg-gray-50/80">매매기준율 (KRW)</th>
            <th class="text-right bg-gray-50/80">전일대비</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="3" class="text-center py-20"><span class="loading loading-spinner text-primary"></span></td>
          </tr>
          <tr v-else-if="historyList.length === 0">
            <td colspan="3" class="text-center py-10 text-gray-400 text-sm">데이터가 없습니다.</td>
          </tr>
          <tr v-else v-for="(item, idx) in historyList" :key="idx" class="hover:bg-blue-50/50 transition-colors border-b border-gray-50 last:border-none">
            <td class="font-mono text-gray-600 text-xs">{{ item.date }}</td>
            <td class="text-right font-bold text-gray-800 text-sm">{{ item.price }}</td>
            <td class="text-right text-sm" :class="item.status === '상승' ? 'text-red-500' : (item.status === '하락' ? 'text-blue-500' : 'text-gray-400')">
              <span v-if="item.status === '상승'" class="text-[10px]">▲</span>
              <span v-if="item.status === '하락'" class="text-[10px]">▼</span>
              {{ item.diff }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #e5e7eb; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #d1d5db; }
</style>