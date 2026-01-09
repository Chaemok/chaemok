<script setup>
import { ref, computed, watch } from 'vue'
import api from '@/api'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement,
  LineElement, Title, Tooltip, Legend, Filler
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const props = defineProps({
  isOpen: Boolean,
  indexInfo: Object // { name: 'NASDAQ', symbol: '^IXIC' }
})
const emit = defineEmits(['close'])

const stockData = ref(null)
const isLoading = ref(false)
const selectedPeriod = ref('1mo')
const startDate = ref('')
const endDate = ref('')

const periods = [
  { label: '1주', value: '5d' },
  { label: '1개월', value: '1mo' },
  { label: '6개월', value: '6mo' },
  { label: '1년', value: '1y' }
]

// 🐜 심볼에 따른 단위(Unit) 결정 함수
const getUnit = (symbol) => {
  if (!symbol) return ''
  if (symbol === 'USDKRW=X') return '원'
  if (symbol === 'GC=F') return '$'
  // 나머지는 지수이므로 포인트(pt)
  return 'pt'
}

// 단위 포맷팅 (예: 2,500.50 pt)
const formatValue = (val) => {
  if (val === undefined || val === null) return '-'
  const num = Number(val).toLocaleString(undefined, { maximumFractionDigits: 2 })
  const unit = getUnit(props.indexInfo?.symbol)
  
  if (unit === '$') return `$${num}`
  return `${num} ${unit}`
}

const fetchData = async () => {
  if (!props.indexInfo?.symbol) return
  isLoading.value = true
  try {
    const params = { period: selectedPeriod.value }
    if (selectedPeriod.value === 'custom') {
      params.start = startDate.value; params.end = endDate.value; delete params.period
    }
    const res = await api.get(`finlife/market/stock/${props.indexInfo.symbol}/`, { params })
    stockData.value = res.data
  } catch (e) { stockData.value = null } 
  finally { isLoading.value = false }
}

watch([() => props.isOpen, selectedPeriod], ([isOpen]) => {
  if (isOpen) fetchData()
})

const onDateChange = () => {
  if (startDate.value && endDate.value) {
    selectedPeriod.value = 'custom'
    fetchData()
  }
}

const chartData = computed(() => {
  if (!stockData.value?.history) return null
  return {
    labels: stockData.value.history.map(d => d.date),
    datasets: [{
      label: props.indexInfo.name,
      data: stockData.value.history.map(d => d.close),
      borderColor: '#4f46e5', 
      backgroundColor: (ctx) => {
        const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, 300)
        gradient.addColorStop(0, 'rgba(79, 70, 229, 0.2)')
        gradient.addColorStop(1, 'rgba(79, 70, 229, 0)')
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

// 🐜 차트 옵션 (툴팁 커스터마이징)
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: { 
    legend: { display: false },
    tooltip: {
      backgroundColor: 'rgba(17, 24, 39, 0.9)', // 어두운 배경
      padding: 12,
      cornerRadius: 12,
      titleFont: { size: 13, weight: 'bold' },
      bodyFont: { size: 14, weight: 'bold' },
      callbacks: {
        title: (context) => `📅 ${context[0].label}`,
        label: (context) => {
          const val = context.raw
          return ` ${props.indexInfo.name}: ${formatValue(val)}`
        }
      }
    }
  },
  scales: { 
    x: { display: false },
    y: { 
      grid: { color: '#f3f4f6' },
      ticks: { callback: (v) => v.toLocaleString() } 
    }
  },
  interaction: { mode: 'index', intersect: false }
}))

const tableData = computed(() => stockData.value?.history ? [...stockData.value.history].reverse() : [])
</script>

<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="emit('close')">
      <div class="bg-white w-full max-w-4xl rounded-[2.5rem] overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        
        <div class="p-6 bg-indigo-600 text-white shrink-0 relative flex justify-between items-center shadow-lg z-10">
          <div class="flex items-center gap-4">
            <h3 class="text-2xl font-black flex items-center gap-2">
              {{ indexInfo?.name }} 
              <span class="text-xs opacity-60 font-medium bg-indigo-800 px-2 py-1 rounded-lg">{{ indexInfo?.symbol }}</span>
            </h3>
            
            <div v-if="stockData" class="flex flex-col">
              <span class="text-xl font-black">{{ formatValue(stockData.current) }}</span>
              <span class="text-xs font-bold" :class="stockData.change >= 0 ? 'text-indigo-200' : 'text-blue-300'">
                {{ stockData.change >= 0 ? '▲' : '▼' }} {{ Math.abs(stockData.change).toLocaleString() }}
              </span>
            </div>
          </div>
          <button @click="emit('close')" class="w-10 h-10 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center text-white transition-colors text-lg">✕</button>
        </div>

        <div class="p-6 overflow-y-auto custom-scrollbar flex-1 space-y-8 bg-slate-50/50">
          
          <div class="flex flex-wrap justify-center gap-4">
            <div class="flex gap-1 bg-white p-1 rounded-xl shadow-sm border border-slate-100">
              <button v-for="p in periods" :key="p.value" @click="selectedPeriod = p.value"
                class="px-4 py-2 rounded-lg text-xs font-bold transition-all"
                :class="selectedPeriod === p.value ? 'bg-indigo-50 text-indigo-600' : 'text-slate-400 hover:text-slate-600'">
                {{ p.label }}
              </button>
            </div>
            <div class="flex items-center gap-2 bg-white p-2 rounded-xl border border-slate-200 shadow-sm">
               <input type="date" v-model="startDate" @change="onDateChange" class="bg-transparent text-xs font-bold text-slate-600 focus:outline-none" />
               <span class="text-slate-300">~</span>
               <input type="date" v-model="endDate" @change="onDateChange" class="bg-transparent text-xs font-bold text-slate-600 focus:outline-none" />
            </div>
          </div>

          <div class="bg-white rounded-[2rem] p-6 shadow-sm border border-slate-100 h-[350px] relative">
            <Line v-if="!isLoading && chartData" :data="chartData" :options="chartOptions" />
            <div v-else class="absolute inset-0 flex flex-col items-center justify-center space-y-2">
              <span class="loading loading-spinner w-10 text-indigo-600"></span>
              <span class="text-[10px] font-bold text-indigo-300 animate-pulse">LOADING CHART...</span>
            </div>
          </div>

          <div class="bg-white border border-slate-100 rounded-[2rem] overflow-hidden shadow-sm">
            <div class="p-4 border-b border-slate-50 bg-slate-50/30">
              <h4 class="text-sm font-black text-slate-700">📜 상세 기록</h4>
            </div>
            <div class="max-h-[300px] overflow-y-auto custom-scrollbar">
              <table class="w-full text-sm text-center">
                <thead class="bg-white text-slate-400 sticky top-0 z-10 shadow-sm">
                  <tr>
                    <th class="py-3 font-bold">일시</th>
                    <th class="py-3 font-bold">종가</th>
                    <th class="py-3 font-bold">거래량</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                  <tr v-for="row in tableData" :key="row.date" class="hover:bg-indigo-50/50 transition-colors">
                    <td class="py-2.5 text-slate-500 font-bold text-xs">{{ row.date }}</td>
                    <td class="py-2.5 font-black text-slate-700">{{ formatValue(row.close) }}</td>
                    <td class="py-2.5 text-slate-400 font-medium text-xs">{{ Number(row.volume).toLocaleString() }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 5px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>