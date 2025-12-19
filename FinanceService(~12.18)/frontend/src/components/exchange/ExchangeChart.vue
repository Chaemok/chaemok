<script setup>
// ... (imports 기존과 동일) ...
import { ref, watch, onMounted, computed, defineEmits } from 'vue'
import axios from 'axios'
import { useFinanceStore } from '@/stores/finance'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler)

// ... (props, emit, periods 기존과 동일) ...
const store = useFinanceStore()
const props = defineProps({
  currency: { type: String, required: true },
  period: { type: String, default: '1mo' }
})
const emit = defineEmits(['update:period'])

const periods = [
  { label: '1주일', value: '1w' },
  { label: '1개월', value: '1mo' },   
  { label: '2개월', value: '2mo' }, 
  { label: '3개월', value: '3mo' }, 
  { label: '6개월', value: '6mo' },
  { label: '12개월', value: '1y' }, 
]

const getPeriodIndex = (val) => {
  const idx = periods.findIndex(p => p.value === val)
  return idx === -1 ? 1 : idx 
}
const sliderValue = ref(getPeriodIndex(props.period))

const chartData = ref({ labels: [], datasets: [] })
const isLoading = ref(false)
const latestPrice = ref(0) 
const priceChange = ref(0) 
const priceChangeRate = ref(0) 

const currentPeriodLabel = computed(() => periods[sliderValue.value]?.label || '')

const moveLeft = () => { if (sliderValue.value > 0) sliderValue.value-- }
const moveRight = () => { if (sliderValue.value < periods.length - 1) sliderValue.value++ }
const setSlider = (index) => { sliderValue.value = index }

watch(sliderValue, (newVal) => {
  const newPeriod = periods[newVal].value
  emit('update:period', newPeriod)
  fetchChartData(newPeriod)
})

const getFlagEmoji = (currencyCode) => {
  const codeMap = {
    'USD': '🇺🇸', 'JPY(100)': '🇯🇵', 'EUR': '🇪🇺', 'CNY': '🇨🇳',
    'GBP': '🇬🇧', 'AUD': '🇦🇺', 'CAD': '🇨🇦', 'NZD': '🇳🇿',
    'HKD': '🇭🇰', 'SGD': '🇸🇬', 'CHF': '🇨🇭',
  }
  return codeMap[currencyCode] || '🌐'
}

// ✨ 통화 기호 매핑 함수 (컴포넌트마다 넣어줌)
const getSymbol = (code) => {
  const symbols = {
    'USD': '$', 'JPY(100)': '¥', 'EUR': '€', 'CNY': '¥', 'GBP': '£',
    'AUD': 'A$', 'CAD': 'C$', 'HKD': 'HK$', 'SGD': 'S$', 'NZD': 'NZ$',
    'CHF': '₣', 'THB': '฿', 'VND': '₫', 'TWD': 'NT$', 'KRW': '₩'
  }
  return symbols[code] || ''
}

const fetchChartData = async (periodVal) => {
  // ... (데이터 fetching 로직 기존과 동일) ...
  isLoading.value = true
  try {
    const res = await axios.get(`${store.API_URL}/api/finances/exchange-rate/chart-data/`, {
      params: { symbol: props.currency, period: periodVal }
    })
    
    const prices = res.data.data
    const dates = res.data.labels
    
    if (prices.length > 0) {
      const current = prices[prices.length - 1]
      const prev = prices.length > 1 ? prices[prices.length - 2] : current
      
      latestPrice.value = current
      priceChange.value = current - prev
      priceChangeRate.value = ((current - prev) / prev) * 100
      
      const gradientColor = (ctx) => {
        const canvas = ctx.chart.ctx
        const gradient = canvas.createLinearGradient(0, 0, 0, 300)
        gradient.addColorStop(0, priceChange.value >= 0 ? 'rgba(239, 68, 68, 0.2)' : 'rgba(59, 130, 246, 0.2)') 
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0)')
        return gradient
      }
      const lineColor = priceChange.value >= 0 ? '#ef4444' : '#3b82f6' 

      chartData.value = {
        labels: dates,
        datasets: [{
          label: '매매기준율',
          data: prices,
          borderColor: lineColor, 
          backgroundColor: gradientColor,
          borderWidth: 2,
          tension: 0.2, 
          pointRadius: 0, 
          pointHoverRadius: 6,
          pointBackgroundColor: lineColor,
          fill: true,
        }]
      }
    }
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false }, tooltip: { mode: 'index', intersect: false } },
  scales: { x: { display: false }, y: { display: true, position: 'right', grid: { display: false } } },
  interaction: { mode: 'nearest', axis: 'x', intersect: false }
}))

const handleWheel = (event) => {
  if (event.deltaY < 0) moveLeft()
  else moveRight()
}

onMounted(() => fetchChartData(props.period))
watch(() => props.currency, () => fetchChartData(periods[sliderValue.value].value))

const formatNumber = (num) => num ? Number(num).toLocaleString(undefined, { maximumFractionDigits: 2 }) : '0'
</script>

<template>
  <div class="bg-white shadow-xl border border-gray-100 rounded-[2rem] p-8 h-full flex flex-col relative overflow-visible">
    
    <div class="mb-4 flex justify-between items-start">
       <div>
         <div class="flex items-center gap-2 mb-1">
           <span class="text-3xl">{{ getFlagEmoji(currency) }}</span>
           <h3 class="font-extrabold text-lg text-gray-500 flex items-center gap-1">
             <span class="text-gray-400 font-normal mr-1">{{ getSymbol(currency) }}</span>
             {{ currency.replace('(100)', '') }}/KRW
           </h3>
         </div>
         <div class="flex items-end gap-3">
           <span class="text-4xl font-black text-gray-900 tracking-tight">{{ formatNumber(latestPrice) }}</span>
           <span class="text-lg font-bold mb-1" :class="priceChange >= 0 ? 'text-red-500' : 'text-blue-500'">
             {{ priceChange >= 0 ? '▲' : '▼' }} {{ formatNumber(Math.abs(priceChange)) }} ({{ priceChangeRate.toFixed(2) }}%)
           </span>
         </div>
       </div>
       <span class="badge badge-lg font-bold bg-gray-100 text-gray-600 border-none">{{ currentPeriodLabel }}</span>
    </div>

    <div 
      class="flex-1 w-full min-h-[300px] relative mb-10 cursor-crosshair"
      @wheel.prevent="handleWheel"
    >
      <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-white/80 z-10">
        <span class="loading loading-spinner loading-lg text-gray-300"></span>
      </div>
      <Line v-if="chartData.datasets.length > 0" :data="chartData" :options="chartOptions" />
    </div>

    <div class="absolute bottom-6 left-1/2 -translate-x-1/2 w-1/2 flex items-center gap-4 select-none">      
      <button @click="moveLeft" class="btn btn-circle btn-xs bg-gray-100 text-gray-500 border-none hover:bg-gray-200">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="currentColor" class="w-3 h-3"><path stroke-linecap="round" stroke-linejoin="round" d="M18 12H6" /></svg>
      </button>

      <div class="flex-1 relative flex items-center h-6 cursor-pointer group" @click.stop>
        <div class="absolute w-full h-1 bg-gray-200 rounded-full"></div>
        <div class="absolute h-1 bg-blue-500 rounded-full transition-all duration-300 ease-out z-0 pointer-events-none" :style="{ width: `calc(${(sliderValue / (periods.length - 1)) * 100}%)` }"></div>
        <div class="absolute w-full h-full flex justify-between items-center pointer-events-none px-0.5">
           <div v-for="(p, index) in periods" :key="index" class="w-1 h-1 rounded-full transition-colors duration-300" :class="index <= sliderValue ? 'bg-white' : 'bg-gray-400'"></div>
        </div>
        <div class="absolute top-1/2 -translate-y-1/2 w-3 h-5 bg-white border border-gray-300 shadow-md rounded-[4px] cursor-grab active:cursor-grabbing transition-all duration-300 ease-out hover:scale-110 hover:border-blue-500 z-10" :style="{ left: `calc(${(sliderValue / (periods.length - 1)) * 100}% - 6px)` }"></div>
        <div v-for="(p, index) in periods" :key="'click-'+index" class="absolute h-full z-20 cursor-pointer" :style="{ left: `calc(${(index / (periods.length - 1)) * 100}% - 10px)`, width: '20px' }" @click.stop="setSlider(index)"></div>
      </div>

      <button @click="moveRight" class="btn btn-circle btn-xs bg-gray-100 text-gray-500 border-none hover:bg-gray-200">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="currentColor" class="w-3 h-3"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" /></svg>
      </button>
    </div>

  </div>
</template>