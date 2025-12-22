<script setup>
import { onMounted, computed } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import { useAuthStore } from '@/stores/auth'

import HomeHero from '@/components/home/HomeHero.vue'
import HomeQuickMenu from '@/components/home/HomeQuickMenu.vue'
import HomeStatCard from '@/components/home/HomeStatCard.vue'
import HomeRecommend from '@/components/home/HomeRecommend.vue'
import HomeNewsFeed from '@/components/home/HomeNewsFeed.vue'

const financeStore = useFinanceStore()
const authStore = useAuthStore()

const usdRate = computed(() => financeStore.getExchangeRate('USD'))

onMounted(async () => {
  await financeStore.fetchQuickData()
  if (authStore.isLoggedIn) {
    financeStore.fetchRecommendations()
  }
})
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <header class="relative w-full shadow-xl z-0">
      <HomeHero />
    </header>

    <main class="max-w-6xl mx-auto px-6 -mt-40 pb-32 space-y-16 relative z-10">
      
      <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <HomeStatCard 
          title="미국 달러" 
          :value="usdRate?.deal_bas_r || '1,478.6'" 
          unit="KRW" 
          icon="💵" 
          :loading="financeStore.isMainLoading"
        />

        <HomeStatCard 
          title="국제 금시세" 
          :value="financeStore.marketData.metal?.gold" 
          unit="USD/oz" 
          icon="✨" 
          :loading="financeStore.isMarketLoading"
        />

        <HomeStatCard 
          title="코스피 지수" 
          :value="financeStore.marketData.kospi" 
          unit="pts" 
          icon="📊" 
          :loading="financeStore.isMarketLoading"
        />

        <HomeStatCard 
          title="삼성전자" 
          :value="financeStore.marketData.stock?.value" 
          unit="원" 
          icon="🐜" 
          :loading="financeStore.isMarketLoading"
        />
      </section>

      <section class="bg-white rounded-[3.5rem] p-12 shadow-xl shadow-slate-200/50 border border-white">
        <div class="flex items-center gap-3 mb-10">
          <span class="text-2xl">⚡️</span>
          <h3 class="text-2xl font-black text-slate-800 tracking-tighter">빠른 서비스</h3>
        </div>
        <HomeQuickMenu />
      </section>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <div class="lg:col-span-2 space-y-6">
          <div class="flex items-center justify-between px-4">
            <h3 class="text-2xl font-black text-slate-900 tracking-tighter">나를 위한 맞춤 금융 ✨</h3>
            <router-link to="/deposit" class="text-sm font-bold text-blue-600">전체보기</router-link>
          </div>
          <div class="bg-white rounded-[3.5rem] p-10 shadow-xl shadow-slate-200/50 border border-white">
            <HomeRecommend :items="financeStore.recommendations" :isLoading="financeStore.isRecLoading" />
          </div>
        </div>

        <div class="space-y-6">
          <div class="px-4">
            <h3 class="text-2xl font-black text-slate-900 tracking-tighter">실시간 뉴스 📰</h3>
          </div>
          <HomeNewsFeed :news="financeStore.news" :isLoading="financeStore.isMainLoading" />
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.tracking-tighter { letter-spacing: -0.05em; }
</style>