<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const router = useRouter()
const isVisible = ref(false)

onMounted(() => {
  setTimeout(() => isVisible.value = true, 100)
})
</script>

<template>
  <section class="relative pt-24 pb-20 px-6 max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between overflow-hidden">
    <div class="md:w-1/2 z-10 transition-all duration-1000 transform" 
         :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'">
      <span class="text-blue-600 font-bold tracking-widest text-sm uppercase mb-4 block">Smart Ants Finance</span>
      <h1 class="text-6xl md:text-8xl font-black leading-tight tracking-tight mb-6">
        Life on <br>
        <span class="text-blue-600">Finance.</span>
      </h1>
      <p class="text-xl text-gray-500 mb-8 max-w-md leading-relaxed">
        <span v-if="userStore.isLogin">
          <strong>{{ userStore.username }}</strong>님, 오늘의 금융 흐름을 확인하세요.<br>
          실시간 환율과 뉴스가 도착했습니다.
        </span>
        <span v-else>
          복잡한 금융, 스마트 앤츠로 단순하게.<br>
          당신의 자산을 불려줄 최고의 파트너.
        </span>
      </p>
      
      <div class="flex gap-4">
        <button v-if="!userStore.isLogin" @click="router.push({name: 'login'})" 
          class="px-8 py-4 bg-gray-900 text-white rounded-full text-lg font-bold hover:bg-blue-600 transition-colors duration-300 shadow-xl">
          시작하기
        </button>
        <button v-else @click="router.push({name: 'mypage'})" 
           class="px-8 py-4 bg-gray-900 text-white rounded-full text-lg font-bold hover:bg-blue-600 transition-colors duration-300 shadow-xl">
          내 자산 보러가기
        </button>
        <button @click="router.push({name: 'stocks-recommend'})" class="px-8 py-4 bg-gray-100 text-gray-900 rounded-full text-lg font-bold hover:bg-gray-200 transition-colors">
          주식 추천 서비스
        </button>
      </div>
    </div>

    <div class="md:w-1/2 mt-10 md:mt-0 relative flex justify-center">
      <div class="absolute w-[500px] h-[500px] bg-blue-50 rounded-full blur-3xl -z-10 animate-pulse"></div>
      <img src="@/assets/logo.png" alt="Hero Ant" class="w-64 md:w-96 drop-shadow-2xl transition-transform duration-700 hover:scale-105 animate-float" 
           :class="isVisible ? 'opacity-100 scale-100' : 'opacity-0 scale-90'" />
    </div>
  </section>
</template>

<style scoped>
h1 { letter-spacing: -0.05em; }
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}
.animate-float { animation: float 3s ease-in-out infinite; }
</style>