
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

onMounted(() => {
  financeStore.fetchQuickData()
  if (authStore.isLoggedIn) {
    financeStore.fetchRecommendations()
  }
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-6 space-y-12">
    <HomeHero />
    <HomeQuickMenu />

    <section>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <HomeStatCard 
          title="미국 달러" 
          :value="usdRate.deal_bas_r" 
          unit="KRW" 
          :loading="financeStore.isMainLoading"
          icon="💵" 
        />
        <HomeStatCard title="국제 금시세" value="85,240" unit="KRW/g" icon="🟡" />
        <HomeStatCard title="코스피 지수" value="2,540.2" unit="pts" icon="📈" />
        <HomeStatCard title="내 자산 수익률" value="+12.5" unit="%" icon="🐜" />
      </div>
    </section>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-10 pb-20">
      <div class="lg:col-span-2">
        <HomeRecommend 
          :items="financeStore.recommendations" 
          :isLoading="financeStore.isRecLoading" 
        />
      </div>
      <div class="lg:col-span-1">
        <HomeNewsFeed 
          :news="financeStore.news" 
          :isLoading="financeStore.isMainLoading" 
        />
      </div>
    </div>
  </div>
</template>