<script setup>
import { onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import { useAuthStore } from '@/stores/auth'

// 컴포넌트 임포트
import HomeHero from '@/components/home/HomeHero.vue'
import HomeMarketTicker from '@/components/home/HomeMarketTicker.vue'
import HomeQuickMenu from '@/components/home/HomeQuickMenu.vue'
import HomeRecommend from '@/components/home/HomeRecommend.vue'
import HomeNewsFeed from '@/components/home/HomeNewsFeed.vue'

const financeStore = useFinanceStore()
const authStore = useAuthStore()

onMounted(async () => {
  // 메인 데이터 로드
  await financeStore.fetchQuickData()
  if (financeStore.fetchMarketStatus) { 
    await financeStore.fetchMarketStatus() 
  }
  // 로그인 상태일 때만 추천 데이터 호출
  if (authStore.isLoggedIn) { 
    financeStore.fetchRecommendations() 
  }
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 font-pretendard">
    <header class="relative w-full h-[500px] md:h-[650px] overflow-hidden shadow-xl z-10">
      <HomeHero />
      <HomeMarketTicker />
    </header>

    <main class="max-w-6xl mx-auto px-4 md:px-6 py-20 space-y-24 relative z-0">
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
        
        <div class="lg:col-span-2 space-y-6">
          <div class="flex items-center gap-3 px-2">
            <span class="bg-blue-600 text-white px-3 py-1 rounded-lg text-xs font-black shadow-lg shadow-blue-200">NEWS</span>
            <h3 class="text-2xl font-black text-slate-900 tracking-tight">금융 헤드라인 📰</h3>
          </div>
          <div class="bg-white rounded-[2.5rem] p-8 shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100">
            <HomeNewsFeed :news="financeStore.news" :isLoading="financeStore.isMainLoading" />
          </div>
        </div>

        <div class="space-y-6">
          <h3 class="text-2xl font-black text-slate-900 tracking-tight px-2">인기 상품 🔥</h3>
          <div class="bg-white rounded-[2.5rem] p-8 shadow-xl border border-blue-50">
            <ul class="space-y-6">
              <li v-for="i in 3" :key="i" class="flex items-center gap-4 group cursor-pointer">
                <span class="text-xl font-black text-blue-600">0{{ i }}</span>
                <div>
                  <p class="text-xs text-slate-400 font-bold">KB국민은행</p>
                  <p class="font-bold text-slate-800 group-hover:text-blue-600 transition-colors">KB Star 정기예금</p>
                </div>
              </li>
            </ul>
            <button class="w-full mt-8 py-4 bg-slate-50 rounded-2xl text-sm font-bold text-slate-600 hover:bg-slate-100 transition-colors">전체보기</button>
          </div>
        </div>
      </div>

      <section class="space-y-8 pb-10">
        <h3 class="text-2xl font-black text-slate-900 tracking-tight px-6">나를 위한 예/적금 맞춤 추천 ✨</h3>
        <div class="bg-white rounded-[3.5rem] p-10 shadow-xl border border-slate-100">
          <HomeRecommend 
            :items="financeStore.recommendations" 
            :message="financeStore.recommendationMessage"
            :isLoading="financeStore.isRecLoading" 
          />
        </div>
</section>
    </main>
  </div>
</template>

<style scoped>
.tracking-tight { letter-spacing: -0.025em; }
</style>