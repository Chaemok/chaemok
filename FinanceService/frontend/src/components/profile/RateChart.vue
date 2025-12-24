<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  joinedProducts: Array // 가입한 상품 목록
})

// 🐜 차트 데이터 가공
const chartData = computed(() => {
  const labels = props.joinedProducts.map(p => p.product.fin_prdt_nm)
  const basicRates = props.joinedProducts.map(p => p.intr_rate)
  const maxRates = props.joinedProducts.map(p => p.intr_rate2)

  return {
    labels,
    datasets: [
      {
        label: '기본 금리 (%)',
        data: basicRates,
        backgroundColor: '#94a3b8', // slate-400
        borderRadius: 6,
      },
      {
        label: '최고 우대 금리 (%)',
        data: maxRates,
        backgroundColor: '#2563eb', // blue-600
        borderRadius: 6,
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: '내 가입 상품 금리 비교 📊' }
  },
  scales: {
    y: { beginAtZero: true, grid: { color: '#f1f5f9' } },
    x: { grid: { display: false } }
  }
}
</script>

<template>
  <div class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-slate-100 h-full min-h-[300px]">
    <div v-if="joinedProducts.length > 0" class="h-[250px]">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
    <div v-else class="h-full flex flex-col items-center justify-center text-slate-400">
      <p class="font-bold">가입한 상품이 없습니다 🐜</p>
    </div>
  </div>
</template>