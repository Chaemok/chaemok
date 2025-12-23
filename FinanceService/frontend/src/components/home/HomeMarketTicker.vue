<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useFinanceStore } from '@/stores/finance'

const financeStore = useFinanceStore()
const now = ref(new Date())
let timer = null

// 티커 데이터 변환
const tickerItems = computed(() => {
  const data = financeStore.marketData
  if (!data || Object.keys(data).length === 0) return []
  return Object.entries(data).map(([label, info]) => ({
    label, value: info.value, change: info.change, rate: info.rate, isUp: info.isUp
  }))
})

// 시간 포맷 (모바일에서는 시/분만 보여줘서 공간 확보)
const formattedTime = computed(() => {
  return now.value.toLocaleTimeString('ko-KR', {
    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
  })
})

onMounted(() => { timer = setInterval(() => { now.value = new Date() }, 1000) })
onUnmounted(() => { if (timer) clearInterval(timer) })
</script>

<template>
  <div class="absolute bottom-0 left-0 w-full bg-slate-900/90 backdrop-blur-xl border-t border-white/10 z-20 overflow-hidden">
    <div class="flex items-center justify-between h-12 md:h-16 px-4 md:px-6">
      
      <div class="flex-1 overflow-hidden">
        <div v-if="tickerItems.length > 0" 
             class="flex items-center gap-8 md:gap-16 animate-ticker whitespace-nowrap hover:[animation-play-state:paused] cursor-pointer">
          <div v-for="n in 2" :key="n" class="flex items-center gap-8 md:gap-16">
            <div v-for="item in tickerItems" :key="item.label" class="flex items-center gap-4 md:gap-6">
              <span class="text-[9px] md:text-[10px] font-black text-slate-500 uppercase">{{ item.label }}</span>
              <span class="text-xs md:text-sm font-bold text-white">{{ item.value }}</span>
              <div :class="['flex items-center px-1.5 py-0.5 rounded-sm text-[9px] md:text-[10px] font-black', 
                           item.isUp ? 'text-emerald-400 bg-emerald-400/10' : 'text-rose-400 bg-rose-400/10']">
                <span>{{ item.isUp ? '▲' : '▼' }} {{ item.change }}</span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-slate-500 text-[10px] animate-pulse">Connecting...</div>
      </div>

      <div class="flex items-center gap-2 md:gap-3 pl-4 md:pl-8 border-l border-white/10 text-[9px] md:text-[10px] font-bold text-slate-400 tracking-widest whitespace-nowrap">
        <span class="relative flex h-1.5 w-1.5 md:h-2 md:w-2">
          <span class="animate-ping absolute h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-1.5 w-1.5 md:h-2 md:w-2 bg-emerald-500"></span>
        </span>
        <span class="hidden sm:inline">LIVE •</span> {{ formattedTime }}
      </div>
    </div>
  </div>
</template>