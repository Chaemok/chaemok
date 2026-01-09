<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '@/api'
import PageHeader from '@/components/common/PageHeader.vue' // 🐜
import MarketTabs from '@/components/market/MarketTabs.vue' // 🐜
import SpotControls from '@/components/spot/SpotControls.vue'
import SpotChart from '@/components/spot/SpotChart.vue'
import SpotTable from '@/components/spot/SpotTable.vue'

const selectedAsset = ref('GOLD')
const startDate = ref('')
const endDate = ref('')
const chartDataList = ref([])
const isLoading = ref(false)

const initDates = () => {
  const end = new Date()
  const start = new Date()
  start.setMonth(start.getMonth() - 1)
  endDate.value = end.toISOString().split('T')[0]
  startDate.value = start.toISOString().split('T')[0]
}

const fetchData = async () => {
  if (!startDate.value || !endDate.value) return
  if (startDate.value > endDate.value) return alert('시작일은 종료일보다 빨라야 합니다.')

  isLoading.value = true
  try {
    const res = await api.get('finlife/spot-history/', {
      params: { type: selectedAsset.value, start: startDate.value, end: endDate.value }
    })
    chartDataList.value = res.data
  } catch (e) {
    chartDataList.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(() => { initDates(); fetchData(); })
watch(selectedAsset, () => fetchData())
</script>

<template>
  <div>
    <PageHeader 
      title="Commodities Market" 
      subtitle="국제 금/은 선물(Futures) 시세를 실시간으로 추적하세요."
      bgClass="bg-yellow-600" 
    />

    <div class="max-w-7xl mx-auto px-4 pb-20 -mt-8 relative z-20">
      <MarketTabs />

      <div class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div class="bg-white rounded-[2.5rem] shadow-xl shadow-slate-200/50 p-6 md:p-8 border border-white space-y-8">
          <div class="flex flex-wrap items-center justify-between gap-y-4 gap-x-6">
            <h3 class="text-xl font-black text-slate-800 flex items-center gap-2 whitespace-nowrap">
              <span v-if="selectedAsset === 'GOLD'" class="text-2xl">🥇</span>
              <span v-else class="text-2xl">🥈</span>
              {{ selectedAsset === 'GOLD' ? '국제 금 시세' : '국제 은 시세' }} 차트
            </h3>
            <div class="w-full xl:w-auto">
              <SpotControls 
                v-model:startDate="startDate"
                v-model:endDate="endDate"
                v-model:selectedAsset="selectedAsset"
                @search="fetchData"
              />
            </div>
          </div>
          <SpotChart :historyData="chartDataList" :assetType="selectedAsset" :isLoading="isLoading" />
        </div>
        <div class="bg-white rounded-[2.5rem] shadow-lg shadow-slate-200/30 p-8 border border-white">
          <h3 class="text-lg font-black text-slate-700 mb-6 px-2">상세 가격 내역</h3>
          <SpotTable :historyData="chartDataList" />
        </div>
      </div>
    </div>
  </div>
</template>