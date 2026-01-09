<script setup>
// 🐜 [수정 핵심] 이 라인이 없어서 에러가 났던 거야!
import { onMounted, ref } from 'vue'

// 프론트엔드에서 넘겨받을 데이터 정의
const props = defineProps({
  title: String,
  value: [String, Number],
  unit: String,
  icon: String,
  loading: Boolean
})

// 컴포넌트가 로드될 때 실행될 로직 (필요할 경우)
onMounted(() => {
  console.log(`${props.title} 카드 준비 완료! 🐜`)
})
</script>

<template>
  <div class="relative group overflow-hidden bg-white/80 backdrop-blur-xl p-6 rounded-[2.5rem] border border-white shadow-xl shadow-slate-200/50 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300">
    
    <div v-if="loading" class="animate-pulse space-y-4">
      <div class="flex justify-between items-center">
        <div class="h-4 w-20 bg-slate-200 rounded"></div>
        <div class="h-8 w-8 bg-slate-100 rounded-full"></div>
      </div>
      <div class="h-10 w-32 bg-slate-200 rounded-xl"></div>
    </div>

    <div v-else class="relative z-10">
      <div class="flex justify-between items-start mb-4">
        <span class="text-[11px] font-black text-slate-400 uppercase tracking-widest">{{ title }}</span>
        <span class="text-2xl group-hover:scale-125 transition-transform duration-500">{{ icon }}</span>
      </div>
      
      <div class="flex items-baseline gap-1">
        <h3 class="text-3xl font-black text-slate-900 tracking-tighter">
          {{ value || '0' }}
        </h3>
        <span class="text-sm font-bold text-slate-400">{{ unit }}</span>
      </div>

      <div class="mt-4 w-full h-1 bg-slate-50 rounded-full overflow-hidden">
        <div class="h-full bg-blue-500 w-0 group-hover:w-full transition-all duration-700"></div>
      </div>
    </div>

    <div class="absolute -right-4 -bottom-4 text-6xl opacity-[0.03] group-hover:opacity-[0.07] transition-opacity">
      {{ icon }}
    </div>
  </div>
</template>

<style scoped>
/* 🐜 폰트 가독성을 위한 설정 */
.tracking-tighter { letter-spacing: -0.05em; }
</style>