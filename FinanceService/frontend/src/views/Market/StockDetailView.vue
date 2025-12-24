<template>
  <div class="space-y-8 animate-in fade-in duration-700">
    <div v-if="stockData" class="bg-white rounded-[2.5rem] p-8 shadow-sm border border-slate-100">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div class="space-y-2">
          <span class="inline-block px-3 py-1 bg-slate-100 text-slate-500 text-[10px] font-black rounded-full uppercase tracking-widest">
            Market Intelligence
          </span>
          <h2 class="text-4xl font-black text-[#1e3a8a] tracking-tighter flex items-center gap-3">
            {{ $route.params.code }}
            <span class="text-lg text-slate-400 font-bold uppercase">{{ stockData.symbol }}</span>
          </h2>
          <p class="text-slate-400 text-xs font-bold">실시간 데이터는 API 제공 환경에 따라 지연될 수 있습니다.</p>
        </div>
        
        <div class="text-right">
          <p class="text-xs font-black text-slate-400 mb-2 uppercase tracking-tighter">Current Price</p>
          <div class="flex items-center justify-end gap-4">
            <span :class="stockData.change >= 0 ? 'text-rose-500' : 'text-blue-600'" class="text-5xl font-black tracking-tighter">
              {{ formatNumber(stockData.current) }}
            </span>
            <div class="flex flex-col items-end">
              <span :class="stockData.change >= 0 ? 'text-rose-500' : 'text-blue-600'" class="text-sm font-black">
                {{ stockData.change >= 0 ? '▲' : '▼' }} {{ Math.abs(stockData.change).toLocaleString() }}
              </span>
              <span class="text-[10px] font-bold text-slate-400">Since 7 days ago</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-[3.5rem] p-10 shadow-xl shadow-blue-900/5 border border-slate-50 relative overflow-hidden min-h-[550px]">
      <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-[#1e3a8a] to-[#2563eb]"></div>
      
      <div class="flex justify-between items-start mb-10">
        <div>
          <h3 class="text-2xl font-black text-slate-800 tracking-tighter">주가 변동 추이</h3>
          <p class="text-slate-400 text-sm font-bold">최근 7일간 1시간 단위 종가 기준</p>
        </div>
        <button @click="fetchStockDetail" class="p-3 bg-slate-50 hover:bg-slate-100 rounded-2xl transition-colors">
          <span class="text-xl">🔄</span>
        </button>
      </div>

      <div class="h-[400px] relative">
        <Line v-if="!isLoading && chartData" :data="chartData" :options="chartOptions" />
        
        <div v-else-if="isLoading" class="absolute inset-0 flex flex-col items-center justify-center space-y-4">
          <div class="relative w-16 h-16">
            <span class="loading loading-spinner w-16 text-[#1e3a8a] opacity-20"></span>
            <div class="absolute inset-0 flex items-center justify-center text-2xl animate-bounce">🐜</div>
          </div>
          <p class="text-[#1e3a8a] font-black text-[11px] uppercase tracking-[0.3em] animate-pulse">Analyzing Market Data...</p>
        </div>

        <div v-else class="h-full flex flex-col items-center justify-center text-center">
          <span class="text-5xl mb-4">🚫</span>
          <p class="text-slate-400 font-bold">데이터를 불러올 수 없습니다.<br>티커명을 확인해 주세요.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement,
  LineElement, Title, Tooltip, Legend, Filler
} from 'chart.js'

// Chart.js 필수 구성 요소 등록
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const route = useRoute()
const stockData = ref(null)
const isLoading = ref(true)

const formatNumber = (val) => new Intl.NumberFormat().format(val)

const fetchStockDetail = async () => {
  isLoading.value = true
  try {
    // 🐜 route.params.code에 '삼성전자' 같은 한글이 들어와도 백엔드에서 처리됨
    const code = route.params.code
    const res = await api.get(`finlife/market/stock/${code}/`)
    stockData.value = res.data
  } catch (err) {
    console.error('Stock Data Error:', err) // 이미지 에러 발생 지점
    stockData.value = null
  } finally {
    isLoading.value = false
  }
}

// 🐜 Chart.js 데이터 구성 (Deep Blue 테마 적용)
const chartData = computed(() => {
  if (!stockData.value) return null
  
  return {
    labels: stockData.value.labels,
    datasets: [{
      label: 'Price',
      data: stockData.value.prices,
      borderColor: '#2563eb', // Ants Blue
      backgroundColor: (context) => {
        const ctx = context.chart.ctx
        const gradient = ctx.createLinearGradient(0, 0, 0, 400)
        gradient.addColorStop(0, 'rgba(37, 99, 235, 0.2)')
        gradient.addColorStop(1, 'rgba(37, 99, 235, 0)')
        return gradient
      },
      borderWidth: 4,
      pointRadius: 0,
      pointHoverRadius: 8,
      pointHoverBackgroundColor: '#1e3a8a',
      pointHoverBorderColor: '#fff',
      pointHoverBorderWidth: 3,
      fill: true,
      tension: 0.4 // 부드러운 곡선 효과
    }]
  }
})

// 🐜 차트 옵션 설정
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#1e3a8a',
      padding: 15,
      cornerRadius: 15,
      titleFont: { size: 12, weight: 'bold' },
      bodyFont: { size: 14, weight: 'black' },
      callbacks: {
        label: (context) => ` 현재가: ${formatNumber(context.raw)}원`
      }
    }
  },
  scales: {
    x: { display: false },
    y: {
      grid: { color: 'rgba(0,0,0,0.03)', drawBorder: false },
      ticks: { 
        font: { size: 11, weight: 'bold' }, 
        color: '#94a3b8',
        callback: (value) => formatNumber(value)
      }
    }
  }
}

onMounted(fetchStockDetail)

// 🐜 다른 종목 검색 시 데이터 즉시 갱신
watch(() => route.params.code, fetchStockDetail)
</script>