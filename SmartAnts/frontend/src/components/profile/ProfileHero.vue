<script setup>
import { ref, computed } from 'vue'
import UserAvatar from '@/components/auth/UserAvatar.vue' 

const props = defineProps({
  user: Object
})

const isHidden = ref(false)

const riskLabel = computed(() => {
  const levels = {
    1: '안정형 🐢', 2: '안정추구형 🐇', 3: '위험중립형 🦊', 
    4: '적극투자형 🐯', 5: '공격투자형 🦅'
  }
  return levels[props.user?.risk_appetite] || '성향 미설정 🌱'
})

const personaSlogan = computed(() => {
  const slogans = {
    1: '티끌 모아 태산! 차곡차곡 쌓는 성실한 저축왕',
    5: '높은 수익을 향해 달리는 야수의 심장'
  }
  return slogans[props.user?.risk_appetite] || '스마트한 금융 생활의 시작'
})

const toggleHidden = () => { isHidden.value = !isHidden.value }
</script>

<template>
  <div class="bg-slate-900 w-full relative overflow-hidden flex flex-col items-center pt-12 pb-40 px-6 transition-all">
    
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
      <div class="absolute top-[-10%] right-[-5%] w-96 h-96 bg-blue-600 rounded-full mix-blend-multiply filter blur-[100px] opacity-20 animate-pulse"></div>
      <div class="absolute bottom-[-10%] left-[-10%] w-96 h-96 bg-indigo-600 rounded-full mix-blend-multiply filter blur-[100px] opacity-20"></div>
    </div>

    <div class="w-full max-w-5xl flex flex-col md:flex-row items-center justify-between gap-8 relative z-10">
      
      <div class="flex flex-col items-center md:items-start text-center md:text-left gap-6">
        <div class="flex items-center gap-5">
          <div class="p-1 bg-gradient-to-tr from-blue-500 to-indigo-500 rounded-full shadow-lg shadow-blue-900/50">
            <UserAvatar 
              :image="user?.profile_image" 
              :name="user?.nickname || user?.username" 
              sizeClass="w-20 h-20 md:w-24 md:h-24 text-3xl"
              class="border-4 border-slate-900"
            />
          </div>
          
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <h1 class="text-2xl md:text-3xl font-black text-white tracking-tight">
                {{ user?.nickname || '부지런한 개미' }}
                <span class="text-blue-400 text-lg align-top">.</span>
              </h1>
              <span class="px-2 py-1 bg-white/10 backdrop-blur rounded text-[10px] font-bold text-blue-200 border border-white/5">
                {{ riskLabel }}
              </span>
            </div>
            <p class="text-slate-400 text-sm font-medium">
              {{ personaSlogan }}
            </p>
          </div>
        </div>

        <div class="flex gap-2 mt-2">
          <router-link :to="{ name: 'profile-edit' }" 
            class="px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-slate-300 text-xs font-bold hover:bg-white/10 hover:text-white transition-all flex items-center gap-1">
            ✏️ 프로필 수정
          </router-link>
          <router-link :to="{ name: 'profile-detail' }" 
            class="px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-slate-300 text-xs font-bold hover:bg-white/10 hover:text-white transition-all flex items-center gap-1">
            🔒 상세 정보
          </router-link>
          <router-link :to="{ name: 'password-change' }" 
            class="px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-slate-300 text-xs font-bold hover:bg-white/10 hover:text-white transition-all flex items-center gap-1">
            🔑 비번 변경
          </router-link>
        </div>
      </div>

      <div class="flex flex-col items-center md:items-end gap-2">
        <div 
          @click="toggleHidden"
          class="flex items-center gap-2 text-slate-400 text-xs font-bold cursor-pointer hover:text-white transition-colors select-none"
        >
          <span>나의 운용 자산</span>
          <span>{{ isHidden ? '🙈' : '👁️' }}</span>
        </div>
        
        <div class="text-4xl md:text-5xl font-black text-white tracking-tighter">
          <span v-if="isHidden" class="tracking-widest opacity-50">••••••••</span>
          <span v-else>
            {{ user?.money?.toLocaleString() || 0 }}
            <span class="text-2xl text-slate-500 font-bold ml-1">원</span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>