<script setup>
import { computed } from 'vue'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'

// 차트 플러그인 등록
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

// 부모(MyPageView)에게서 '상품 목록'을 받아옵니다.
const props = defineProps({
  products: {
    type: Array,
    default: () => []
  }
})

// 받아온 데이터(products)가 변하면 차트도 자동으로 다시 그려집니다.
const chartData = computed(() => {
  const labels = props.products.map(p => p.product_name)
  const rates = props.products.map(p => p.interest_rate)
  const highRates = props.products.map(p => p.highest_rate)

  return {
    labels: labels,
    datasets: [
      {
        label: '기본 금리',
        backgroundColor: '#3b82f6', // blue-500
        data: rates,
        borderRadius: 4
      },
      {
        label: '최고 우대 금리',
        backgroundColor: '#10b981', // emerald-500
        data: highRates,
        borderRadius: 4
      }
    ]
  }
})

const chartOptions = { 
  responsive: true, 
  maintainAspectRatio: false 
}
</script>

<template>
  <div class="w-full h-full">
    <Bar v-if="products.length > 0" :data="chartData" :options="chartOptions" />
    
    <p v-else class="text-center text-gray-400 flex items-center justify-center h-full">
      데이터가 없어 차트를 표시할 수 없습니다.
    </p>
  </div>
</template>