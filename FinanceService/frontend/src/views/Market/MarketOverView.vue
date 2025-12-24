<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useFinanceStore } from '@/stores/finance'
import HomeStatCard from '@/components/home/HomeStatCard.vue'

const financeStore = useFinanceStore()
const router = useRouter()
const stockSearch = ref('')

// 주식 종목 검색 시 상세 페이지로 이동
const onSearchStock = () => {
  if (!stockSearch.value) return
  router.push({ name: 'stock-detail', params: { code: stockSearch.value.toUpperCase() } })
}
</script>

<template>
  <div class="space-y-12">
    <div class="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-[3rem] p-12 text-white shadow-xl">
      <h2 class="text-3xl font-black mb-4">어떤 종목이 궁금하세요? 🐜</h2>
      <p class="text-blue-100 mb-8 font-medium">티커(예: TSLA, AAPL) 또는 종목명을 입력하여 상세 차트를 확인하세요.</p>
      
      <div class="relative max-w-2xl">
        <input 
          v-model="stockSearch"
          @keyup.enter="onSearchStock"
          type="text" 
          placeholder="삼성전자 또는 NVDA 입력..."
          class="w-full py-5 px-8 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 text-white placeholder:text-blue-200 focus:outline-none focus:bg-white/20 transition-all font-bold"
        />
        <button @click="onSearchStock" class="absolute right-4 top-1/2 -translate-y-1/2 bg-white text-blue-600 px-6 py-2 rounded-xl font-black text-sm hover:bg-blue-50 transition-colors">
          조회하기
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <HomeStatCard 
        v-for="(info, label) in financeStore.marketData" 
        :key="label"
        :title="label"
        :value="info.value"
        :unit="info.rate"
        :icon="info.isUp ? '📈' : '📉'"
        :loading="financeStore.isMarketLoading"
      />
    </div>
  </div>
</template>