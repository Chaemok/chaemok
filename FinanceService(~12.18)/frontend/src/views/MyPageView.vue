<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import axios from 'axios'

// 컴포넌트 임포트
import PageHeader from '@/components/layout/PageHeader.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import AssetChart from '@/components/AssetChart.vue' // 분리한 차트 컴포넌트

const userStore = useUserStore()
const router = useRouter()
const joinedProducts = ref([])
const isLoading = ref(true)

onMounted(() => {
  // 내 가입 상품 가져오기
  axios({
    method: 'get',
    url: `${userStore.API_URL}/api/finances/joined-products/`, // 주소 변수 사용
    headers: { Authorization: `Bearer ${userStore.token}` }
  })
  .then((res) => {
    joinedProducts.value = res.data
    isLoading.value = false
  })
  .catch((err) => {
    console.log(err)
    isLoading.value = false
  })
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-8 mb-20">
    
    <PageHeader 
      title="마이페이지" 
      subtitle="내 자산 현황과 포트폴리오를 한눈에 관리하세요." 
    />

    <div class="mb-8 p-6 rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-700 text-white shadow-lg flex flex-col md:flex-row justify-between items-center gap-6">
      <div class="flex items-center gap-5">
        <div class="w-20 h-20 rounded-full border-4 border-white/30 overflow-hidden bg-white/10 flex items-center justify-center">
           <img v-if="userStore.profileImage" 
                :src="userStore.profileImage.startsWith('http') ? userStore.profileImage : `${userStore.API_URL}${userStore.profileImage}`" 
                class="w-full h-full object-cover" />
           <span v-else class="text-3xl font-bold text-white">
             {{ userStore.username.substring(0,2).toUpperCase() }}
           </span>
        </div>
        
        <div>
          <div class="text-blue-100 text-sm mb-1">Welcome back!</div>
          <h2 class="text-3xl font-bold">
            {{ userStore.nickname || userStore.username }}님
          </h2>
          <p class="text-blue-100 mt-1 opacity-90">
            총 <span class="font-bold text-white">{{ joinedProducts.length }}개</span>의 금융 상품을 구독 중입니다.
          </p>
        </div>
      </div>
      
      <button 
        @click="router.push({ name: 'profile' })"
        class="px-6 py-3 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 transition-all font-medium text-sm flex items-center gap-2 backdrop-blur-sm"
      >
        <span>내 정보 관리</span>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
      </button>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      
      <section>
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-bold text-gray-800 flex items-center gap-2">
            📋 가입한 상품
          </h3>
          <span v-if="joinedProducts.length > 0" class="text-xs font-bold bg-blue-100 text-blue-600 px-2 py-1 rounded-full">
            {{ joinedProducts.length }}개
          </span>
        </div>
        
        <div v-if="isLoading" class="space-y-3">
          <div v-for="i in 3" :key="i" class="h-20 bg-gray-100 rounded-xl animate-pulse"></div>
        </div>

        <div v-else-if="joinedProducts.length > 0" class="space-y-3">
          <BaseCard 
            v-for="product in joinedProducts" 
            :key="product.id"
            class="!p-5 cursor-pointer hover:ring-2 hover:ring-blue-500 hover:ring-offset-2 transition-all group border border-gray-100 shadow-sm"
            @click="router.push({name: 'deposit-detail', params: {id: product.id}})"
          >
            <div class="flex justify-between items-center">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-xs">
                  BANK
                </div>
                <div>
                  <p class="text-xs text-gray-400 font-bold mb-0.5">{{ product.bank_name }}</p>
                  <p class="font-bold text-gray-800 text-lg group-hover:text-blue-600 transition-colors">
                    {{ product.product_name }}
                  </p>
                </div>
              </div>
              <div class="text-right bg-emerald-50 px-3 py-1.5 rounded-lg">
                <span class="text-xs text-emerald-600 block font-medium">최고 금리</span>
                <span class="text-xl font-bold text-emerald-600">{{ product.highest_rate }}%</span>
              </div>
            </div>
          </BaseCard>
        </div>

        <BaseCard v-else class="text-center py-16 bg-gray-50/50 border-2 border-dashed border-gray-200 shadow-none">
          <div class="text-5xl mb-4">🏦</div>
          <p class="text-gray-900 font-bold text-lg">아직 가입한 상품이 없어요</p>
          <p class="text-gray-500 mb-6 text-sm">나에게 딱 맞는 예적금 상품을 찾아보세요!</p>
          <BaseButton color="blue" @click="router.push({name: 'deposits'})">
            상품 추천 받으러 가기
          </BaseButton>
        </BaseCard>
      </section>

      <section>
        <h3 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          📊 금리 한눈에 보기
        </h3>
        
        <BaseCard class="h-[500px] flex items-center justify-center p-6 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-32 h-32 bg-blue-50 rounded-bl-full -mr-10 -mt-10 opacity-50"></div>
          
          <AssetChart :products="joinedProducts" />
        </BaseCard>
      </section>

    </div>
  </div>
</template>