<script setup>
defineProps({
  rates: { type: Array, default: () => [] },
  nowTime: { type: String, default: '' },
  isLoading: Boolean
})

const formatNumber = (num) => num ? Number(num).toLocaleString() : '0'
</script>

<template>
  <div class="bg-white border border-gray-200 rounded-[2rem] p-8 shadow-sm hover:shadow-xl transition-shadow duration-500 flex flex-col h-full">
    <div class="flex items-center gap-3 mb-6">
      <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-2xl">🌏</div>
      <div class="flex-1"> 
        <div class="flex items-center justify-between"> 
          <div class="flex items-center gap-2">
            <h2 class="text-2xl font-bold">실시간 환율</h2>
            <span class="bg-red-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full animate-pulse">LIVE</span>
          </div>
        </div>
        <div class="flex items-center gap-2 mt-1">
          <p class="text-gray-500 text-sm">네이버 금융 기준</p>
          <span v-if="nowTime" class="text-xs text-gray-400 bg-gray-100 px-2 py-0.5 rounded-md">
            {{ nowTime }} 기준
          </span>
        </div>
      </div>
    </div> 
    
    <div v-if="isLoading" class="flex-1 flex items-center justify-center text-gray-400">
      <span class="loading loading-spinner text-primary"></span>
    </div>
    <div v-else class="space-y-3">
      <div v-for="(rate, index) in rates" :key="index" 
           class="flex items-center justify-between p-4 bg-gray-50 rounded-2xl hover:bg-gray-100 transition-colors">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center border text-lg shadow-sm">
            {{ rate.name.includes('미국') ? '🇺🇸' : rate.name.includes('일본') ? '🇯🇵' : rate.name.includes('유럽') ? '🇪🇺' : '🇨🇳' }}
          </div>
          <div>
            <p class="font-bold text-gray-900">{{ rate.name }}</p>
            <p class="text-xs text-gray-500">매매기준율</p>
          </div>
        </div>
        <div class="text-right">
          <p class="text-xl font-bold text-gray-900">{{ formatNumber(rate.value) }}원</p>
          <p class="text-sm font-semibold" :class="rate.is_up ? 'text-red-500' : 'text-blue-500'">
             {{ rate.is_up ? '▲' : '▼' }} {{ rate.change }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>