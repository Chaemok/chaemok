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
  
  return Object.entries(data)
    .filter(([_, info]) => info !== null) 
    .map(([label, info]) => ({
      label, 
      value: info.value, 
      change: info.change, 
      rate: info.rate, 
      isUp: info.isUp
    }))
})

// 🐜 [수정] 현재 시간이 아니라, "시장 기준 시간"을 표시
// 평일 낮이면 현재 시간, 밤이나 주말이면 "장 마감(Close)" 표시 로직
const marketStatusText = computed(() => {
  const current = now.value
  return `LIVE • ${current.toLocaleTimeString('ko-KR', { 
    hour: '2-digit', 
    minute: '2-digit', 
    second: '2-digit', 
    hour12: false 
  })}`
  
  /* 원래 코드는 주석 처리 또는 잠시 지워두기
  const current = now.value
  const day = current.getDay()
  const hour = current.getHours()
  if (day === 0 || day === 6 || hour < 9 || hour >= 16) {
    return `CLOSED • ${current.toLocaleDateString()}`
  }
  return `LIVE • ${current.toLocaleTimeString('ko-KR', { 
    hour: '2-digit', 
    minute: '2-digit', 
    second: '2-digit', 
    hour12: false 
  })}`
  */
})

onMounted(() => { timer = setInterval(() => { now.value = new Date() }, 1000) })
onUnmounted(() => { if (timer) clearInterval(timer) })
</script>

<template>
  <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-screen bg-slate-900/95 backdrop-blur-xl border-t border-white/10 z-20 overflow-hidden">
    
    <div class="flex items-center justify-between h-14 px-6 md:px-10 max-w-[1920px] mx-auto">
      
      <div class="flex-1 overflow-hidden mask-image-linear">
        <div v-if="tickerItems.length > 0" 
             class="flex items-center gap-12 md:gap-20 animate-ticker whitespace-nowrap hover:[animation-play-state:paused] cursor-pointer">
          <div v-for="n in 2" :key="n" class="flex items-center gap-12 md:gap-20">
            <div v-for="item in tickerItems" :key="item.label" class="flex items-center gap-4">
              <span class="text-[10px] md:text-xs font-black text-slate-500 uppercase tracking-wider">{{ item.label }}</span>
              <span class="text-sm md:text-base font-bold text-white tabular-nums">{{ item.value }}</span>
              <div :class="['flex items-center px-1.5 py-0.5 rounded text-[10px] font-bold', 
                           item.isUp ? 'text-emerald-400 bg-emerald-400/10' : 'text-rose-400 bg-rose-400/10']">
                <span>{{ item.isUp ? '▲' : '▼' }} {{ item.change }}</span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-slate-500 text-xs font-medium animate-pulse flex items-center gap-2">
          <span class="w-2 h-2 bg-slate-500 rounded-full"></span>
          Market data connecting...
        </div>
      </div>

      <div class="flex items-center gap-3 pl-6 md:pl-10 border-l border-white/10 ml-6 text-[10px] md:text-xs font-bold text-slate-400 tracking-widest whitespace-nowrap">
        <span class="relative flex h-2 w-2">
          <span v-if="marketStatusText.includes('LIVE')" class="animate-ping absolute h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span :class="['relative inline-flex rounded-full h-2 w-2', marketStatusText.includes('LIVE') ? 'bg-emerald-500' : 'bg-slate-500']"></span>
        </span>
        {{ marketStatusText }}
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 좌우 끝을 부드럽게 가려주는 마스크 효과 */
.mask-image-linear {
  mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
}
</style>