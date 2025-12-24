<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

// 🐜 분리한 컴포넌트 3총사 임포트
import SpotControls from '@/components/spot/SpotControls.vue'
import SpotChart from '@/components/spot/SpotChart.vue'
import SpotTable from '@/components/spot/SpotTable.vue' // 👈 [추가] 표 컴포넌트

// 상태 변수
const selectedAsset = ref('GOLD')
const startDate = ref('')
const endDate = ref('')
const chartDataList = ref([])
const isLoading = ref(false)

// 날짜 초기화 (최근 1달)
const initDates = () => {
  const end = new Date()
  const start = new Date()
  start.setMonth(start.getMonth() - 1)
  endDate.value = end.toISOString().split('T')[0]
  startDate.value = start.toISOString().split('T')[0]
}

// 데이터 요청
const fetchData = async () => {
  if (!startDate.value || !endDate.value) return
  if (startDate.value > endDate.value) return alert('시작일은 종료일보다 빨라야 합니다.')

  isLoading.value = true
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/finlife/spot-history/', {
      params: { type: selectedAsset.value, start: startDate.value, end: endDate.value }
    })
    chartDataList.value = res.data
  } catch (e) {
    console.error(e)
    alert('시세 데이터를 불러오지 못했습니다.')
  } finally {
    isLoading.value = false
  }
}

// 초기 실행 및 감시
onMounted(() => { initDates(); fetchData(); })
watch(selectedAsset, () => fetchData())
</script>

<template>
  <div class="min-h-screen bg-slate-50 py-12 px-4 font-pretendard">
    <div class="max-w-6xl mx-auto">
      
      <div class="text-center mb-10 space-y-2">
        <h1 class="text-4xl font-black text-slate-900">원자재 시세 조회 🪙</h1>
        <p class="text-slate-500">국제 금/은 선물(Futures) 가격을 차트와 표로 확인하세요.</p>
      </div>

      <SpotControls 
        v-model:startDate="startDate"
        v-model:endDate="endDate"
        v-model:selectedAsset="selectedAsset"
        @search="fetchData"
      />

      <SpotChart 
        :historyData="chartDataList" 
        :assetType="selectedAsset" 
        :isLoading="isLoading"
      />

      <SpotTable :historyData="chartDataList" />

    </div>
  </div>
</template>

<style scoped>
.font-pretendard { font-family: 'Pretendard', sans-serif; }
</style>