<script setup>
import { ref, computed } from 'vue'

const saveAmount = ref(5000) // 기본값 5,000원
const savePeriod = ref(1)    // 기본 1년

const calculatedSavings = computed(() => {
  const rate = 0.035
  const months = savePeriod.value * 12
  const monthly = saveAmount.value * 30
  // 월복리 적금 공식 근사치
  const result = monthly * (months + 1) * months * (rate / 12) / 2 + (monthly * months)
  return Math.floor(result).toLocaleString()
})
</script>

<template>
  <section class="bg-gradient-to-br from-indigo-50 to-blue-50 rounded-[3rem] p-8 md:p-14 border border-blue-100 relative overflow-hidden">
    <div class="relative z-10 flex flex-col md:flex-row items-center gap-10 md:gap-20">
      <div class="flex-1 space-y-6 text-center md:text-left">
        <h3 class="text-3xl font-black text-slate-800 leading-tight">
          매일 커피 한 잔값,<br>
          <span class="text-blue-600">1년 뒤엔 얼마가 될까요?</span>
        </h3>
        <p class="text-slate-500 font-medium">소소한 금액이라도 꾸준히 모으면 큰 자산이 됩니다.<br>슬라이더를 움직여 미래 자산을 확인해보세요.</p>
      </div>
      
      <div class="flex-1 w-full bg-white p-8 rounded-[2rem] shadow-xl">
        <div class="space-y-6">
          <div>
            <label class="block text-xs font-bold text-slate-400 mb-2">매일 저축할 금액</label>
            <div class="flex items-center justify-between mb-2">
              <span class="text-2xl font-black text-slate-800">{{ Number(saveAmount).toLocaleString() }}원</span>
              <span class="text-sm font-bold text-slate-400">/ 일</span>
            </div>
            <input type="range" min="1000" max="50000" step="1000" v-model="saveAmount" class="w-full accent-blue-600 cursor-pointer h-2 bg-slate-100 rounded-lg appearance-none">
          </div>
          
          <div class="pt-6 border-t border-slate-100 text-center">
            <p class="text-sm font-bold text-slate-400 mb-1">{{ savePeriod }}년 뒤 예상 자산 (연 3.5% 기준)</p>
            <p class="text-4xl font-black text-blue-600 tracking-tight">{{ calculatedSavings }}원</p>
          </div>
        </div>
      </div>
    </div>
    <div class="absolute top-0 right-0 text-[300px] opacity-[0.03] pointer-events-none -translate-y-1/3 translate-x-1/4">💰</div>
  </section>
</template>