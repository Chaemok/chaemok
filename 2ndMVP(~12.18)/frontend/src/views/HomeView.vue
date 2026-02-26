<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useFinanceStore } from '@/stores/finance'

// ✨ 컴포넌트 불러오기 (Dashboard 대신 개별 카드 사용)
import HomeHero from '@/components/home/HomeHero.vue'
import HomeQuickLinks from '@/components/home/HomeQuickLinks.vue'
import HomeRecommend from '@/components/home/HomeRecommend.vue'
import HomeLiveRates from '@/components/home/HomeLiveRates.vue' // 👈 NEW
import HomeNewsList from '@/components/home/HomeNewsList.vue'   // 👈 NEW

const userStore = useUserStore()
const financeStore = useFinanceStore()

const recommendedProducts = ref([])
const exchangeRates = ref([]) 
const newsList = ref([])      
const isLoading = ref(true)
const nowTime = ref('') 

const getNowTime = () => {
  const d = new Date()
  const pad = (n) => n < 10 ? '0' + n : n
  return `${d.getFullYear()}/${pad(d.getMonth() + 1)}/${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

onMounted(async () => {
  try {
    const rateRes = await axios.get(`${financeStore.API_URL}/api/finances/exchange-rate/live/`)
    exchangeRates.value = rateRes.data
    nowTime.value = getNowTime()

    const newsRes = await axios.get(`${financeStore.API_URL}/api/finances/news/`)
    newsList.value = newsRes.data

    if (userStore.isLogin) {
      const recommendRes = await axios.get(`${financeStore.API_URL}/api/finances/deposits/recommend/`, {
        headers: { Authorization: `Bearer ${userStore.token}` }
      })
      recommendedProducts.value = recommendRes.data
    }
  } catch (err) {
    console.error(err)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen bg-white font-sans text-gray-900 pb-20">
    
    <HomeHero />
    <HomeQuickLinks />
    <HomeRecommend :products="recommendedProducts" />

    <section class="max-w-7xl mx-auto px-6 mb-20">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
        <HomeLiveRates 
          :rates="exchangeRates" 
          :nowTime="nowTime" 
          :isLoading="isLoading" 
        />
        <HomeNewsList 
          :newsList="newsList" 
          :isLoading="isLoading" 
        />
      </div>
    </section>

  </div>
</template>