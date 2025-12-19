<script setup>
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)

const props = defineProps({
  chartData: Object
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'bottom', labels: { font: { weight: 'bold' } } }
  }
}
</script>

<template>
  <div class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-slate-100 h-full">
    <h3 class="text-lg font-black text-slate-800 mb-6 flex items-center gap-2">
      <span class="w-2 h-5 bg-primary rounded-full"></span> 자산 구성 비중
    </h3>
    <div class="h-[250px]">
      <Pie :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>