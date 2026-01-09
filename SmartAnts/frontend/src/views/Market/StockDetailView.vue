<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement,
  LineElement, Title, Tooltip, Legend, Filler
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const route = useRoute()
const stockData = ref(null)
const isLoading = ref(true)

// 🐜 기간 필터 상태
const selectedPeriod = ref('1d') 
const startDate = ref('')
const endDate = ref('')

const periods = [
  { label: '1일', value: '1d' },
  { label: '1주', value: '5d' },
  { label: '1개월', value: '1mo' },
  { label: '6개월', value: '6mo' },
  { label: '1년', value: '1y' }
]

const formatNumber = (val) => new Intl.NumberFormat().format(val)

const fetchStockDetail = async () => {
  if (!route.params.code) return
  
  isLoading.value = true
  try {
    const params = { period: selectedPeriod.value }
    if (selectedPeriod.value === 'custom' && startDate.value && endDate.value) {
      params.start = startDate.value
      params.end = endDate.value
      // custom일 땐 period 파라미터 제거 (백엔드 로직에 맞게)
      delete params.period
    }

    const res = await api.get(`finlife/market/stock/${route.params.code}/`, { params })
    stockData.value = res.data
  } catch (err) {
    console.error('Stock Data Error:', err)
    stockData.value = null
  } finally {
    isLoading.value = false
  }
}

// 기간 버튼 클릭 시
const setPeriod = (period) => {
  selectedPeriod.value = period
  startDate.value = ''
  endDate.value = ''
  fetchStockDetail()
}

// 날짜 직접 선택 시
const onDateChange = () => {
  if (startDate.value && endDate.value) {
    if (startDate.value > endDate.value) return alert("시작일이 종료일보다 늦을 수 없습니다.")
    selectedPeriod.value = 'custom'
    fetchStockDetail()
  }
}

// 차트 데이터 구성
const chartData = computed(() => {
  if (!stockData.value?.history) return null
  return {
    labels: stockData.value.history.map(d => d.date),
    datasets: [{
      label: 'Price',
      data: stockData.value.history.map(d => d.close),
      borderColor: '#2563eb',
      backgroundColor: (ctx) => {
        const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, 400)
        gradient.addColorStop(0, 'rgba(37, 99, 235, 0.2)')
        gradient.addColorStop(1, 'rgba(37, 99, 235, 0)')
        return gradient
      },
      borderWidth: 3,
      pointRadius: 0,
      pointHoverRadius: 6,
      fill: true,
      tension: 0.3
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: { legend: { display: false } },
  scales: {
    x: { display: false },
    y: { grid: { color: '#f1f5f9' }, ticks: { callback: (v) => v.toLocaleString() } }
  }
}

// 표 데이터 (최신순 정렬)
const tableData = computed(() => {
  if (!stockData.value?.history) return []
  return [...stockData.value.history].reverse()
})

onMounted(fetchStockDetail)
watch(() => route.params.code, fetchStockDetail)
</script>

<template>
  <div class="space-y-8 animate-in fade-in duration-700">
    
    <div v-if="stockData" class="bg-white rounded-[2.5rem] p-8 shadow-sm border border-slate-100">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div class="space-y-2">
          <span class="inline-block px-3 py-1 bg-slate-100 text-slate-500 text-[10px] font-black rounded-full uppercase tracking-widest">
            Stock Analysis
          </span>
          <h2 class="text-4xl font-black text-[#1e3a8a] tracking-tighter flex items-center gap-3">
            {{ stockData.name }}
            <span class="text-lg text-slate-400 font-bold uppercase">{{ stockData.symbol }}</span>
          </h2>
        </div>
        
        <div class="text-right">
          <p class="text-xs font-black text-slate-400 mb-2 uppercase tracking-tighter">Current Price</p>
          <div class="flex items-center justify-end gap-4">
            <span :class="stockData.change >= 0 ? 'text-rose-500' : 'text-blue-600'" class="text-5xl font-black tracking-tighter">
              {{ formatNumber(stockData.current) }}
              <span class="text-lg text-slate-400 font-medium">{{ stockData.currency }}</span>
            </span>
            <div class="flex flex-col items-end">
              <span :class="stockData.change >= 0 ? 'text-rose-500' : 'text-blue-600'" class="text-sm font-black">
                {{ stockData.change >= 0 ? '▲' : '▼' }} {{ Math.abs(stockData.change).toLocaleString() }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-[3rem] p-8 shadow-xl shadow-blue-900/5 border border-slate-50 relative overflow-hidden min-h-[500px]">
      
      <div class="flex flex-wrap items-center justify-between gap-4 mb-8">
        <div class="flex gap-1 bg-slate-100 p-1.5 rounded-2xl">
          <button 
            v-for="p in periods" :key="p.value"
            @click="setPeriod(p.value)"
            class="px-4 py-2 rounded-xl text-xs font-bold transition-all"
            :class="selectedPeriod === p.value ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'"
          >
            {{ p.label }}
          </button>
        </div>
        
        <div class="flex items-center gap-2 bg-slate-50 p-2 rounded-2xl border border-slate-100">
          <input type="date" v-model="startDate" @change="onDateChange" class="bg-transparent text-xs font-bold text-slate-600 p-1 focus:outline-none" />
          <span class="text-slate-300">~</span>
          <input type="date" v-model="endDate" @change="onDateChange" class="bg-transparent text-xs font-bold text-slate-600 p-1 focus:outline-none" />
        </div>
      </div>

      <div class="h-[400px] relative">
        <Line v-if="!isLoading && chartData" :data="chartData" :options="chartOptions" />
        
        <div v-else-if="isLoading" class="absolute inset-0 flex flex-col items-center justify-center space-y-4 bg-white/80 z-10">
          <span class="loading loading-spinner w-12 text-[#1e3a8a]"></span>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-[2.5rem] shadow-lg border border-slate-100 overflow-hidden">
      <div class="p-6 border-b border-slate-100">
        <h3 class="text-lg font-black text-slate-800">📊 상세 거래 내역</h3>
      </div>
      <div class="overflow-x-auto max-h-[500px] custom-scrollbar">
        <table class="w-full text-sm text-center">
          <thead class="bg-slate-50 text-slate-500 sticky top-0 z-10">
            <tr>
              <th class="py-4 font-black">일시</th>
              <th class="py-4 font-black">종가</th>
              <th class="py-4 font-black">시가</th>
              <th class="py-4 font-black">고가</th>
              <th class="py-4 font-black">저가</th>
              <th class="py-4 font-black">거래량</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="row in tableData" :key="row.date" class="hover:bg-slate-50/50 transition-colors">
              <td class="py-3 font-bold text-slate-600">{{ row.date }}</td>
              <td class="py-3 font-black text-slate-800">{{ formatNumber(row.close) }}</td>
              <td class="py-3 text-slate-500">{{ formatNumber(row.open) }}</td>
              <td class="py-3 text-rose-400">{{ formatNumber(row.high) }}</td>
              <td class="py-3 text-blue-400">{{ formatNumber(row.low) }}</td>
              <td class="py-3 font-bold text-slate-400">{{ formatNumber(row.volume) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
</style>