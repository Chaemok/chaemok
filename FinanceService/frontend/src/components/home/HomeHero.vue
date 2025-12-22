<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const slides = [
  {
    id: 1,
    title: "똑똑한 개미들의",
    highlight: "데이터 금융 놀이터",
    description: "흩어진 내 자산 정보를 한눈에 확인하고,\n최적의 금융 전략을 AI로 분석받으세요. 🐜",
    image: "/src/assets/hero-bg-1.jpg", 
    label: "Smart Financial Intelligence"
  },
  {
    id: 2,
    title: "가장 가까운",
    highlight: "전국 은행/증권사 찾기",
    description: "내 위치 기반으로 가장 빠르게 방문 가능한\n금융 기관과 최적의 경로를 안내합니다. 📍",
    image: "/src/assets/hero-bg-2.jpg", 
    label: "Location Based Service"
  },
  {
    id: 3,
    title: "나만을 위한",
    highlight: "맞춤형 예적금 추천",
    description: "복잡한 금리 비교는 이제 그만,\n나의 자산 상황에 딱 맞는 상품을 골라드려요. ✨",
    image: "/src/assets/hero-bg-3.jpg", 
    label: "Personalized Curation"
  }
]

const currentSlide = ref(0)
let timer = null

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % slides.length
}

const startTimer = () => {
  stopTimer()
  timer = setInterval(nextSlide, 5000)
}

const stopTimer = () => {
  if (timer) clearInterval(timer)
}

onMounted(() => startTimer())
onUnmounted(() => stopTimer())
</script>

<template>
  <div class="relative w-full min-h-[750px] flex items-center justify-center overflow-hidden bg-transparent">
    
    <transition-group name="bg-slide">
      <div v-for="(slide, index) in slides" :key="'bg-' + slide.id" 
           v-show="currentSlide === index"
           class="absolute inset-0 z-0">
        <img :src="slide.image" class="w-full h-full object-cover zoom-animation" />
        <div class="absolute inset-0 bg-gradient-to-b from-blue-950/90 via-blue-900/40 to-transparent"></div>
      </div>
    </transition-group>

    <transition-group name="content-slide">
      <div v-for="(slide, index) in slides" :key="'content-' + slide.id"
           v-show="currentSlide === index"
           class="absolute inset-0 flex items-center justify-center z-10">
        
        <div class="text-center space-y-8 px-4 pb-20 max-w-4xl mx-auto">
          <div class="stagger-1 inline-block px-4 py-1.5 bg-blue-500/20 rounded-full backdrop-blur-md border border-white/10">
            <span class="text-blue-200 text-[10px] font-black tracking-[0.3em] uppercase">{{ slide.label }}</span>
          </div>
          
          <h1 class="stagger-2 text-5xl md:text-7xl font-black text-white leading-[1.1] tracking-tighter">
            {{ slide.title }}<br/>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-200 to-white">
              {{ slide.highlight }}
            </span>
          </h1>
          
          <p class="stagger-3 text-white/70 text-lg md:text-xl font-medium leading-relaxed whitespace-pre-line">
            {{ slide.description }}
          </p>

          <div class="stagger-4 pt-8 flex flex-wrap items-center justify-center gap-4">
            <button class="px-10 py-5 bg-white text-blue-950 rounded-2xl font-black shadow-2xl hover:scale-105 active:scale-95 transition-all">
              {{ index === 1 ? '지도 바로가기' : '내 자산 분석하기' }}
            </button>
            <button class="px-10 py-5 bg-white/10 text-white rounded-2xl font-black backdrop-blur-md border border-white/20 hover:bg-white/20 transition-all">
              가이드 보기
            </button>
          </div>
        </div>
      </div>
    </transition-group>

    <div class="absolute bottom-48 left-1/2 -translate-x-1/2 z-20 flex gap-3">
      <button v-for="(_, index) in slides" :key="index"
              @click="currentSlide = index; startTimer();"
              class="w-2.5 h-2.5 rounded-full transition-all duration-500"
              :class="currentSlide === index ? 'bg-white w-8' : 'bg-white/30'"></button>
    </div>
  </div>
</template>

<style scoped>
.zoom-animation { animation: slowZoom 20s infinite alternate ease-in-out; }
@keyframes slowZoom {
  from { transform: scale(1.05); }
  to { transform: scale(1.15); }
}

/* =========================================
   🐜 다이나믹 슬라이드 애니메이션 (이거임!)
========================================= */

/* 배경: 부드러운 페이드 + 살짝 움직임 */
.bg-slide-enter-active, .bg-slide-leave-active { transition: opacity 1.5s ease, transform 1.5s ease; }
.bg-slide-enter-from { opacity: 0; transform: scale(1.1); }
.bg-slide-leave-to { opacity: 0; transform: scale(0.95); }

/* 컨텐츠: 오른쪽에서 들어오고 왼쪽으로 나가는 다이나믹 슬라이드 */
.content-slide-enter-active { transition: all 1s cubic-bezier(0.23, 1, 0.32, 1); }
.content-slide-leave-active { transition: all 0.8s cubic-bezier(0.75, 0, 0.175, 1); }

/* 들어올 때: 오른쪽에서 80px 떨어진 곳에서 스르륵 */
.content-slide-enter-from { opacity: 0; transform: translateX(80px); }
/* 나갈 때: 왼쪽으로 80px 밀려나며 사라짐 */
.content-slide-leave-to { opacity: 0; transform: translateX(-80px); }

/* 🐜 개별 요소 시차(Stagger) 효과 */
.content-slide-enter-active .stagger-1 { transition-delay: 0.1s; }
.content-slide-enter-active .stagger-2 { transition-delay: 0.2s; }
.content-slide-enter-active .stagger-3 { transition-delay: 0.3s; }
.content-slide-enter-active .stagger-4 { transition-delay: 0.4s; }

.tracking-tighter { letter-spacing: -0.05em; }
</style>