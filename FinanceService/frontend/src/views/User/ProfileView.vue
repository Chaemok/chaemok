<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

// 🐜 컴포넌트 기반 구조화
import ProfileHero from '@/components/profile/ProfileHero.vue'
import AssetChartCard from '@/components/profile/AssetChartCard.vue'
import PostListItem from '@/components/community/PostListItem.vue'

const router = useRouter()
const authStore = useAuthStore()
const joinedProducts = ref([])
const myPosts = ref([])
const isLoading = ref(true)

// 🐜 채목이가 정한 커뮤니티 카테고리 설정 (PostListItem 재사용용)
const categoryConfig = {
  inquiry: { label: '1:1 문의', class: 'bg-slate-100 text-slate-500' },
  free: { label: '자유', class: 'bg-indigo-50 text-primary' },
  review: { label: '후기', class: 'bg-amber-50 text-amber-600' },
  qna: { label: 'Q&A', class: 'bg-emerald-50 text-emerald-600' },
  tips: { label: '꿀팁', class: 'bg-purple-50 text-purple-600' },
  faq: { label: 'FAQ', class: 'bg-blue-50 text-blue-600' }
}

// 🐜 자산 비중 차트 데이터 (Chart.js용)
const assetData = computed(() => ({
  labels: ['예금', '적금', '주식', '현금'],
  datasets: [{
    backgroundColor: ['#4F46E5', '#818CF8', '#C7D2FE', '#E0E7FF'],
    hoverOffset: 10,
    data: [40, 20, 30, 10] // 실무에서는 가입 상품 금액에 따라 계산 로직 추가 가능
  }]
}))

// 🐜 백엔드 데이터 통합 로드 (Django DRF 연동)
const fetchData = async () => {
  try {
    const [prodRes, postRes] = await Promise.all([
      api.get('finlife/joined-products/'),
      api.get('community/posts/') // 쿼리 파라미터로 내 글만 필터링하거나 별도 endpoint 사용
    ])
    
    // 내가 쓴 글만 필터링 (백엔드 로직에 따라 수정 가능)
    joinedProducts.value = prodRes.data.joined_deposits || []
    myPosts.value = postRes.data.filter(p => p.user_nickname === authStore.user?.nickname)
  } catch (err) {
    console.error('마이페이지 데이터 로드 실패:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  if (authStore.isLoggedIn) {
    fetchData()
  } else {
    router.push('/login')
  }
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 pb-24">
    <div class="max-w-6xl mx-auto px-4 py-10 space-y-8">
      
      <ProfileHero :user="authStore.user" />

      <div class="flex justify-end gap-3">
        <router-link to="/profile/edit" class="btn btn-sm bg-white border-slate-200 text-slate-600 rounded-xl font-bold hover:bg-slate-100 shadow-sm">
          ⚙️ 정보 수정
        </router-link>
        <router-link to="/profile/password" class="btn btn-sm bg-white border-slate-200 text-slate-600 rounded-xl font-bold hover:bg-slate-100 shadow-sm">
          🔒 비밀번호 변경
        </router-link>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        
        <div class="lg:col-span-1 sticky top-24">
          <AssetChartCard :chartData="assetData" />
          
          <div class="mt-6 bg-white p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
            <h4 class="font-black text-slate-800 mb-4">가입 상품 현황 🏛️</h4>
            <div class="space-y-3">
              <div class="flex justify-between text-sm">
                <span class="text-slate-400 font-medium">예적금 합계</span>
                <span class="font-bold text-primary">{{ joinedProducts.length }}건</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-slate-400 font-medium">참여 중인 챌린지</span>
                <span class="font-bold text-slate-700">2건</span>
              </div>
            </div>
          </div>
        </div>

        <div class="lg:col-span-2 space-y-6">
          <div class="flex justify-between items-center px-4">
            <h3 class="text-2xl font-black text-slate-800 flex items-center gap-3">
              <span class="w-2 h-8 bg-primary rounded-full"></span> 내가 쓴 글
            </h3>
            <span class="text-sm font-bold text-slate-400 bg-white px-3 py-1 rounded-full shadow-sm">총 {{ myPosts.length }}개</span>
          </div>
          
          <div v-if="isLoading" class="space-y-4">
            <div v-for="n in 3" :key="n" class="h-24 bg-white animate-pulse rounded-[2rem] border border-slate-50"></div>
          </div>

          <div v-else-if="myPosts.length > 0" class="space-y-4">
            <PostListItem 
              v-for="post in myPosts" 
              :key="post.id" 
              :post="post" 
              :categoryConfig="categoryConfig" 
              @click="router.push(`/community/${post.id}`)"
            />
          </div>

          <div v-else class="bg-white p-20 rounded-[3rem] text-center border border-dashed border-slate-200">
            <p class="text-5xl mb-6">🐜</p>
            <p class="text-slate-500 font-bold text-lg mb-6">아직 광장에 남긴 발자국이 없어요.</p>
            <router-link to="/community/create" class="btn btn-primary rounded-2xl px-10">첫 글 쓰러 가기</router-link>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>