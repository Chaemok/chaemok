<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  user: Object
})

const isHidden = ref(false)

// 🐜 1. 성향별 라벨 (뱃지용)
const riskLabel = computed(() => {
  const levels = {
    1: '안정형 🐢', 2: '안정추구형 🐇', 3: '위험중립형 🦊', 
    4: '적극투자형 🐯', 5: '공격투자형 🦅'
  }
  return levels[props.user?.risk_appetite] || '성향 미설정 🌱'
})

// 🐜 2. [NEW] 성향별 맞춤 슬로건 (이메일/가입일 대신 이거!)
const personaSlogan = computed(() => {
  const slogans = {
    1: '티끌 모아 태산! 차곡차곡 쌓는 성실한 저축왕',
    2: '돌다리도 두들겨 보는 신중한 투자자',
    3: '위험과 수익 사이, 완벽한 밸런스의 전략가',
    4: '기회가 보이면 놓치지 않는 스마트한 승부사',
    5: '높은 수익을 향해 달리는 야수의 심장'
  }
  return slogans[props.user?.risk_appetite] || '아직 나만의 투자 스타일을 찾는 중이에요'
})

const toggleHidden = () => { isHidden.value = !isHidden.value }
</script>

<template>
  <div class="bg-primary p-8 md:p-10 text-white rounded-[2.5rem] shadow-xl shadow-primary/20 flex flex-col md:flex-row justify-between items-center gap-8 relative overflow-hidden transition-all hover:shadow-primary/40">
    
    <div class="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full -translate-y-1/2 translate-x-1/4 blur-3xl"></div>

    <div class="flex flex-col md:flex-row items-center gap-6 z-10 text-center md:text-left">
      <div class="relative group cursor-pointer">
        <div class="w-24 h-24 rounded-[2rem] overflow-hidden ring-4 ring-white/20 ring-offset-2 ring-offset-primary transition-transform group-hover:scale-105 shadow-lg">
          <img :src="user?.profile_image || 'https://api.dicebear.com/7.x/avataaars/svg?seed=Felix'" class="w-full h-full object-cover" />
        </div>
        <div class="absolute bottom-0 right-0 bg-white text-primary text-xs font-black px-2 py-0.5 rounded-full shadow-md border-2 border-primary">
          Lv.{{ user?.risk_appetite || 1 }}
        </div>
      </div>
      
      <div class="space-y-2">
        <div class="flex flex-col md:flex-row items-center gap-3">
          <h2 class="text-3xl font-black tracking-tight">{{ user?.nickname || '똑똑한 개미' }}님</h2>
          <span class="px-3 py-1 bg-white/10 backdrop-blur-md rounded-lg text-xs font-bold border border-white/10 text-indigo-100 shadow-sm">
            {{ riskLabel }}
          </span>
        </div>
        
        <div class="flex flex-col md:flex-row items-center gap-2 text-indigo-100/90 text-sm font-medium">
          <span class="opacity-70">@{{ user?.username }}</span>
          <span class="hidden md:inline w-1 h-1 bg-indigo-300 rounded-full"></span>
          <span class="font-bold text-white tracking-wide">
            "{{ personaSlogan }}"
          </span>
        </div>
      </div>
    </div>

    <div class="text-center md:text-right z-10 w-full md:w-auto bg-white/10 p-5 rounded-3xl backdrop-blur-sm border border-white/10 hover:bg-white/15 transition-colors">
      <div class="flex items-center justify-center md:justify-end gap-2 mb-1 text-indigo-100 text-xs font-bold opacity-80 cursor-pointer select-none" @click="toggleHidden">
        <span>현재 설정된 연봉</span>
        <span class="text-lg">{{ isHidden ? '🙈' : '👁️' }}</span>
      </div>
      
      <div class="h-10 flex items-center justify-center md:justify-end">
        <p v-if="!isHidden" class="text-3xl font-black tracking-tight animate-in fade-in slide-in-from-bottom-2">
          {{ (user?.salary || 0).toLocaleString() }}<span class="text-xl font-bold ml-1">원</span>
        </p>
        <p v-else class="text-3xl font-black tracking-widest opacity-50">
          •••••••••
        </p>
      </div>
    </div>

  </div>
</template>