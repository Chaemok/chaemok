<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const slides = [
  { 
    id: 1,
    title: "최고 금리\n예적금 찾기 💰", 
    sub: "은행별 금리 비교부터 나에게 딱 맞는 상품 검색까지.", 
    img: 'hero-bg-2.jpg',
    path: '/deposit',
    btnText: '상품 보러가기'
  },
  { 
    id: 2,
    title: "실시간\n환율 정보 확인 💱", 
    sub: "오늘의 환율을 지금 바로 확인하세요.", 
    img: 'hero-bg-3.jpg',
    path: '/market/exchange-rate',
    btnText: '환율 계산기'
  },
  { 
    id: 3,
    title: "글로벌\n시장 지표 분석 📈", 
    sub: "나스닥, 코스피 등 전 세계 주식 시장의 흐름을 한눈에.", 
    img: 'hero-bg-4.jpg',
    path: '/market',
    btnText: '시장지표 상세'
  },

  { 
    id: 4,
    title: "실시간\n금융 뉴스 📰", 
    sub: "가장 빠르게 전달되는 오늘의 핵심 경제 소식.", 
    img: 'hero-bg-5.jpg',
    path: '/news',
    btnText: '뉴스 더보기'

  },
  // { 
  //   id: 1,
  //   title: "Smart Ants가 추천하는 \n 주식 종목 추천 🤖", 
  //   sub: "데이터 분석으로 찾는 유망 종목.", 
  //   img: 'hero-bg-1.jpg',
  //   path: '/stocks',
  //   btnText: '주식 추천받기'
  // },
]

const currentSlide = ref(0)
let slideTimer = null

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % slides.length
  resetTimer()
}

const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + slides.length) % slides.length
  resetTimer()
}

const resetTimer = () => {
  if (slideTimer) clearInterval(slideTimer)
  slideTimer = setInterval(nextSlide, 6000)
}

const getImageUrl = (name) => {
  try {
    return new URL(`../../assets/${name}`, import.meta.url).href
  } catch (e) {
    return 'https://images.unsplash.com/photo-1611974765270-ca1258634369?q=80&w=2070&auto=format&fit=crop'
  }
}

onMounted(() => resetTimer())
onUnmounted(() => { if (slideTimer) clearInterval(slideTimer) })
</script>

<template>
  <div class="relative w-screen ml-[calc(-50vw+50%)] h-[600px] overflow-hidden text-white bg-slate-950 font-pretendard mb-12">
    
    <Transition name="fade" mode="out-in">
      <div :key="currentSlide" class="absolute inset-0">
        <div class="absolute inset-0 bg-cover bg-center animate-subtle-zoom"
             :style="{ backgroundImage: `url(${getImageUrl(slides[currentSlide].img)})` }">
        </div>
        <div class="absolute inset-0 bg-gradient-to-r from-slate-950/90 via-slate-900/50 to-transparent"></div>
      </div>
    </Transition>

    <div class="max-w-7xl mx-auto px-6 h-full flex flex-col justify-center relative z-20">
      <Transition name="slide-fade" mode="out-in">
        <div :key="currentSlide" class="max-w-2xl space-y-8">
          <h1 class="text-4xl md:text-6xl font-extrabold leading-tight tracking-tight drop-shadow-2xl whitespace-pre-line">
            {{ slides[currentSlide].title }}
          </h1>
          <p class="text-lg md:text-xl text-white/80 font-medium max-w-lg">
            {{ slides[currentSlide].sub }}
          </p>
          
          <router-link :to="slides[currentSlide].path" 
             class="group inline-flex items-center gap-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-full font-bold text-sm hover:shadow-[0_0_20px_rgba(37,99,235,0.4)] transition-all duration-300 transform hover:-translate-y-1">
            {{ slides[currentSlide].btnText }}
            <span class="group-hover:translate-x-1 transition-transform">→</span>
          </router-link>
        </div>
      </Transition>
    </div>

    <button @click="prevSlide" class="absolute left-6 top-1/2 -translate-y-1/2 z-30 p-3 rounded-full bg-white/10 backdrop-blur-md hover:bg-white/20 transition-all border border-white/10 hidden md:block">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" /></svg>
    </button>
    <button @click="nextSlide" class="absolute right-6 top-1/2 -translate-y-1/2 z-30 p-3 rounded-full bg-white/10 backdrop-blur-md hover:bg-white/20 transition-all border border-white/10 hidden md:block">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" /></svg>
    </button>

    <div class="absolute bottom-24 left-1/2 -translate-x-1/2 flex gap-3 z-30">
      <div v-for="(_, index) in slides" :key="index"
           @click="currentSlide = index"
           :class="['h-1.5 transition-all duration-500 rounded-full cursor-pointer', 
                    index === currentSlide ? 'w-10 bg-white' : 'w-2 bg-white/30 hover:bg-white/50']">
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 1s ease-in-out; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.slide-fade-enter-active { transition: all 0.6s ease-out; }
.slide-fade-leave-active { transition: all 0.4s ease-in; }
.slide-fade-enter-from { opacity: 0; transform: translateX(30px); }
.slide-fade-leave-to { opacity: 0; transform: translateX(-20px); }
@keyframes subtle-zoom {
  0% { transform: scale(1); }
  100% { transform: scale(1.1); }
}
.animate-subtle-zoom { animation: subtle-zoom 10s linear infinite alternate; }
</style>