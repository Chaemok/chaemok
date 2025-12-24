<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

// 🐜 컴포넌트 임포트
import ProfileHero from '@/components/profile/ProfileHero.vue' 
import RateChart from '@/components/profile/RateChart.vue' // [교체] 금리 차트
import JoinedProducts from '@/components/profile/JoinedProducts.vue' // [추가] 목록

const authStore = useAuthStore()
const depositList = ref([])
const savingList = ref([])
const isLoading = ref(true)

// 데이터 로드
const fetchJoinedProducts = async () => {
  try {
    const res = await api.get('finlife/joined-products/') // 백엔드 API 호출
    depositList.value = res.data.joined_deposits
    savingList.value = res.data.joined_savings
  } catch (err) {
    console.error('상품 목록 로드 실패', err)
  } finally {
    isLoading.value = false
  }
}

// 차트용 통합 데이터 (예금 + 적금)
const allProducts = computed(() => [...depositList.value, ...savingList.value])

onMounted(() => {
  if (authStore.token) fetchJoinedProducts()
})
</script>

<template>
  <div v-if="authStore.user" class="max-w-5xl mx-auto py-12 px-4 space-y-8 animate-in fade-in duration-700">
    
    <ProfileHero :user="authStore.user" />
    
    <div class="flex justify-end gap-2">
        <router-link to="/profile" class="btn bg-slate-900 text-white rounded-xl font-bold border-none hover:bg-black">
          개인정보 상세 🔒
        </router-link>
        <router-link to="/profile/edit" class="btn bg-white text-slate-600 border-slate-200 rounded-xl font-bold hover:bg-slate-50 hover:border-slate-300">
          프로필 수정 ✏️
        </router-link>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <RateChart :joinedProducts="allProducts" />
      </div>

      <div class="space-y-8 lg:col-span-1 h-[400px] overflow-y-auto custom-scrollbar pr-2">
        <JoinedProducts type="예금" :products="depositList" />
        <JoinedProducts type="적금" :products="savingList" />
      </div>
    </div>

  </div>
  
  <div v-else class="min-h-[50vh] flex flex-col items-center justify-center space-y-4">
    <span class="loading loading-spinner loading-lg text-primary"></span>
    <p class="text-slate-400 font-bold animate-pulse">개미 정보를 불러오는 중입니다... 🐜</p>
  </div>
</template>

<style scoped>
/* 커스텀 스크롤바 */
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background-color: #e2e8f0; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-track { background-color: transparent; }
</style>