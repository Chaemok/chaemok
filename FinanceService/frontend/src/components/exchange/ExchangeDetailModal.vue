<script setup>
import { ref, computed, watch } from 'vue'
import axios from 'axios'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const props = defineProps({
  isOpen: Boolean,
  currencyData: Object
})
const emit = defineEmits(['close'])

// 상태 관리
const historyData = ref([])
const isLoading = ref(false)
const selectedPeriod = ref('1mo') // 기본값
const startDate = ref('') // 직접 선택 시작일
const endDate = ref('')   // 직접 선택 종료일

// 기간 버튼 옵션
const periods = [
  { label: '1주일', value: '5d' },
  { label: '1개월', value: '1mo' },
  { label: '6개월', value: '6mo' },
  { label: '1년', value: '1y' }
]

// 데이터 가져오기
const fetchHistory = async () => {
  if (!props.currencyData?.cur_unit) return
  
  isLoading.value = true
  try {
    const params = { code: props.currencyData.cur_unit }

    // 직접 날짜 선택 모드인지 확인
    if (selectedPeriod.value === 'custom' && startDate.value && endDate.value) {
      params.start = startDate.value
      params.end = endDate.value
    } else {
      params.period = selectedPeriod.value
    }

    const response = await axios.get('http://127.0.0.1:8000/api/finlife/exchange-history/', { params })
    historyData.value = response.data
  } catch (error) {
    console.error('차트 데이터 로드 실패:', error)
    historyData.value = []
  } finally {
    isLoading.value = false
  }
}

// 감시자
watch(
  [() => props.isOpen, () => props.currencyData, selectedPeriod],
  ([isOpen, newData, newPeriod]) => {
    if (isOpen && newData) {
      // 기간 버튼을 누르면 날짜 입력 초기화
      if (newPeriod !== 'custom') {
        startDate.value = ''
        endDate.value = ''
        fetchHistory()
      }
    }
  },
  { immediate: true }
)

// 날짜 선택 시 'custom' 모드로 변경하고 조회
const onDateChange = () => {
  if (startDate.value && endDate.value) {
    if (startDate.value > endDate.value) return alert("시작일이 종료일보다 늦을 수 없습니다.")
    selectedPeriod.value = 'custom' // 버튼 선택 해제 효과
    fetchHistory()
  }
}

// 차트 설정 (기존과 동일)
const chartData = computed(() => {
  if (!historyData.value.length) return { labels: [], datasets: [] }
  return {
    labels: historyData.value.map(d => d.date.slice(5).replace('-', '.')),
    datasets: [{
      label: '매매기준율',
      data: historyData.value.map(d => d.rate),
      borderColor: '#2563eb',
      backgroundColor: (ctx) => {
        const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, 300)
        gradient.addColorStop(0, 'rgba(37, 99, 235, 0.2)')
        gradient.addColorStop(1, 'rgba(37, 99, 235, 0)')
        return gradient
      },
      borderWidth: 2,
      pointRadius: 0,
      pointHoverRadius: 6,
      fill: true,
      tension: 0.2
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: { x: { grid: { display: false }, ticks: { maxTicksLimit: 6 } }, y: { grid: { color: '#f1f5f9' } } },
  interaction: { intersect: false, mode: 'index' }
}

const getFlagUrl = (code) => {
  if (!code) return ''
  let c = code.substring(0, 2).toLowerCase()
  if (code === 'EUR') c = 'eu'
  if (code === 'JPY(100)') c = 'jp'
  if (code === 'CNH') c = 'cn'
  return `https://flagcdn.com/w40/${c}.png`
}
const formatNumber = (num) => Number(num).toLocaleString(undefined, { maximumFractionDigits: 2 })
const recentTableData = computed(() => [...historyData.value].reverse())
</script>

<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="emit('close')">
      <div class="bg-white w-full max-w-2xl rounded-[2.5rem] overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        
        <div class="p-6 bg-blue-600 text-white shrink-0 relative">
          <button @click="emit('close')" class="absolute top-6 right-6 text-white/70 hover:text-white transition-colors">✕</button>
          <div class="flex items-center gap-4">
             <img :src="getFlagUrl(currencyData?.cur_unit)" class="w-12 h-12 rounded-full border-2 border-white/30" />
             <div>
                 <p class="text-sm font-bold opacity-80 mb-0.5">{{ currencyData?.cur_unit }}</p>
                 <h2 class="text-2xl font-black">{{ currencyData?.cur_nm }}</h2>
             </div>
          </div>
        </div>

        <div class="p-6 overflow-y-auto custom-scrollbar flex-1">
          
          <div class="flex flex-col items-center gap-3 mb-6">
            <div class="flex gap-1 bg-slate-100 p-1 rounded-xl">
                <button 
                  v-for="period in periods" 
                  :key="period.value"
                  @click="selectedPeriod = period.value"
                  class="px-3 py-1.5 rounded-lg text-xs font-bold transition-all"
                  :class="selectedPeriod === period.value ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'"
                >
                  {{ period.label }}
                </button>
            </div>
            
            <div class="flex items-center gap-2 text-sm">
               <input type="date" v-model="startDate" @change="onDateChange" class="bg-slate-50 border border-slate-200 rounded-lg p-1.5 font-bold text-slate-600 focus:outline-blue-500" />
               <span class="text-slate-300">~</span>
               <input type="date" v-model="endDate" @change="onDateChange" class="bg-slate-50 border border-slate-200 rounded-lg p-1.5 font-bold text-slate-600 focus:outline-blue-500" />
            </div>
          </div>

          <div class="h-64 bg-slate-50 rounded-2xl p-4 border border-slate-100 relative mb-8">
            <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-slate-50/80 z-10 rounded-2xl">
              <span class="loading loading-spinner text-blue-600"></span>
            </div>
            <Line v-if="chartData.datasets.length" :data="chartData" :options="chartOptions" />
            <div v-else-if="!isLoading" class="flex h-full items-center justify-center text-slate-400">데이터가 없습니다.</div>
          </div>

          <div>
            <h4 class="text-sm font-black text-slate-800 mb-4">📅 일별 시세</h4>
            <div class="border border-slate-100 rounded-2xl overflow-hidden shadow-sm">
              <table class="w-full text-sm text-center">
                <thead class="bg-slate-50 border-b border-slate-100">
                  <tr>
                    <th class="py-3 px-4 font-black text-slate-500">날짜</th>
                    <th class="py-3 px-4 font-black text-slate-500">매매기준율</th>
                    <th class="py-3 px-4 font-black text-slate-500 text-right">전일대비</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                  <tr v-for="(row, index) in recentTableData" :key="row.date">
                    <td class="py-3 px-4 font-bold text-slate-600">{{ row.date }}</td>
                    <td class="py-3 px-4 font-black text-slate-800">{{ formatNumber(row.rate) }}</td>
                    <td class="py-3 px-4 font-bold text-right">
                       <span v-if="index < recentTableData.length - 1">
                           <span v-if="row.rate > recentTableData[index+1].rate" class="text-red-500">▲ {{ formatNumber(row.rate - recentTableData[index+1].rate) }}</span>
                           <span v-else-if="row.rate < recentTableData[index+1].rate" class="text-blue-500">▼ {{ formatNumber(recentTableData[index+1].rate - row.rate) }}</span>
                           <span v-else class="text-slate-400">-</span>
                       </span>
                    </td>
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
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>