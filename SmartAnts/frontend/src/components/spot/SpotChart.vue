<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const props = defineProps({
  historyData: { type: Array, default: () => [] },
  assetType: { type: String, default: 'GOLD' },
  isLoading: Boolean
})

const chartData = computed(() => {
  return {
    labels: props.historyData.map(d => d.date),
    datasets: [{
      label: props.assetType === 'GOLD' ? '금(KRW)' : '은(KRW)',
      data: props.historyData.map(d => d.rate_krw), // 🐜 차트는 원화 기준!
      borderColor: props.assetType === 'GOLD' ? '#d97706' : '#64748b',
      backgroundColor: (ctx) => {
        const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, 400)
        const color = props.assetType === 'GOLD' ? '251, 191, 36' : '148, 163, 184'
        gradient.addColorStop(0, `rgba(${color}, 0.4)`)
        gradient.addColorStop(1, `rgba(${color}, 0)`)
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

// 🐜 툴팁 커스터마이징 (원화 + 달러 동시 표기)
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: { 
    legend: { display: false },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: 'rgba(15, 23, 42, 0.9)', // 어두운 배경
      titleFont: { size: 14 },
      bodyFont: { size: 13 },
      padding: 12,
      cornerRadius: 8,
      callbacks: {
        title: (context) => `📅 ${context[0].label}`,
        label: (context) => {
          // 현재 마우스가 올라간 데이터의 인덱스
          const index = context.dataIndex
          // 원본 데이터에서 해당 인덱스의 정보를 가져옴
          const rawItem = props.historyData[index]
          
          const krw = Number(rawItem.rate_krw).toLocaleString()
          const usd = Number(rawItem.rate_usd).toLocaleString()
          
          // 🐜 두 줄로 보여주기 위해 배열 반환
          return [
            `🇰🇷 ${krw}원`,
            `🇺🇸 $${usd}`
          ]
        }
      }
    }
  },
  scales: { 
    y: { 
      grid: { color: '#f1f5f9' },
      ticks: { callback: (val) => val.toLocaleString() } // Y축 콤마
    }, 
    x: { grid: { display: false }, ticks: { maxTicksLimit: 8 } } 
  },
  interaction: { intersect: false, mode: 'nearest' }
}))
</script>

<template>
  <div class="bg-white rounded-[2.5rem] p-8 shadow-2xl shadow-slate-200/40 border border-slate-100 h-[400px] relative">
    <div v-if="isLoading" class="absolute inset-0 flex flex-col items-center justify-center bg-white/80 z-10 rounded-[2.5rem]">
       <span class="loading loading-spinner loading-lg text-yellow-500"></span>
    </div>
    <div v-else-if="!isLoading && historyData.length === 0" class="flex h-full items-center justify-center text-slate-400">
        데이터가 없습니다.
    </div>
    <Line v-else :data="chartData" :options="chartOptions" />
  </div>
</template>