<script setup>
import { ref, onMounted, computed, inject, watch } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import { useAuthStore } from '@/stores/auth'
import instance from '@/api/index'
import { useRouter } from 'vue-router'

// 컴포넌트 임포트
import HomeHero from '@/components/home/HomeHero.vue'
import HomeMarketTicker from '@/components/home/HomeMarketTicker.vue'
import HomeFeatures from '@/components/home/HomeFeatures.vue'
import HomeSavingsCalculator from '@/components/home/HomeSavingsCalculator.vue'
import HomeRecommend from '@/components/home/HomeRecommend.vue'
import HomeLoginBanner from '@/components/home/HomeLoginBanner.vue'
import DepositDetailModal from '@/components/deposit/DepositDetailModal.vue'

const financeStore = useFinanceStore()
const authStore = useAuthStore()
const router = useRouter()

// App.vue에서 provide한 채팅 열기 함수
const openGlobalChat = inject('openGlobalChat')

// 상태 관리
const loading = ref(false)
const depositItems = ref([]) 
const savingItems = ref([])
const recommendMessage = ref('') // 추천 멘트 저장

// 모달 관련 상태
const showModal = ref(false)
const modalType = ref('deposit')
const selectedItem = ref(null)

const userNickname = computed(() => authStore.nickname || authStore.user?.username || '회원') 

// ✅ 상세 모달 열기
const openDetail = (item, type) => {
  // item 구조가 때로는 { product: {...}, ... } 형태일 수 있으므로 평탄화
  const productData = item.product || item

  selectedItem.value = { 
    ...productData,
    // 옵션 정보가 최상위에 있으면 그대로 사용, 없으면 productData 내부 사용
    intr_rate2: item.intr_rate2 || productData.intr_rate2,   
    intr_rate: item.intr_rate || productData.intr_rate,     
    save_trm: item.save_trm || productData.save_trm,
    // 가입 시 필요한 ID (Option ID)
    id: item.id || productData.id, 
    // 상품 상세 조회를 위한 상품 코드
    fin_prdt_cd: productData.fin_prdt_cd, 
  }
  
  modalType.value = type
  showModal.value = true 
}

// ✅ 추천 알고리즘 API 호출
const fetchRecommendations = async () => {
  if (!authStore.isLoggedIn) return

  loading.value = true
  try {
    const res = await instance.get('/finlife/recommend/')
    
    const responseData = res.data.data || []
    recommendMessage.value = res.data.message || '회원님을 위한 맞춤 추천입니다.'

    const deposits = []
    const savings = []

    responseData.forEach(item => {
      // 🐜 수정된 부분: 백엔드 serializer 구조에 맞춰 데이터 경로 수정
      // item은 Option이고, 그 안에 product 객체가 있음
      const product = item.product || {} 
      const name = product.fin_prdt_nm || ''

      // 이름에 '적금'이 들어가는지로 분류
      if (name.includes('적금')) {
        savings.push(item)
      } else {
        deposits.push(item)
      }
    })

    // 각각 최대 2개(혹은 4개)씩만 잘라서 보여주기
    depositItems.value = deposits.slice(0, 2) 
    savingItems.value = savings.slice(0, 2)

  } catch (err) {
    console.error('추천 로드 실패:', err)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  // 기본 데이터 로드 (환율 등)
  await financeStore.fetchQuickData()
  
  // 시장 지표 로드
  if (financeStore.fetchMarketStatus) { 
    await financeStore.fetchMarketStatus() 
  }

  // 로그인 상태라면 추천 로드
  if (authStore.isLoggedIn) { 
    fetchRecommendations() 
  }
})

// 로그인 상태 변경 감지 (로그인 직후 홈으로 왔을 때 데이터 로드)
watch(() => authStore.isLoggedIn, (isLoggedIn) => {
  if (isLoggedIn) {
    fetchRecommendations()
  } else {
    depositItems.value = []
    savingItems.value = []
  }
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 font-pretendard pb-20">
    
    <header class="relative w-full h-[600px] shadow-xl z-10 mb-16">
      <HomeHero />
      <div class="absolute bottom-0 w-full z-20">
        <HomeMarketTicker />
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 md:px-6 space-y-24 relative z-0">
      
      <div 
        class="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-3xl p-8 text-white shadow-xl flex flex-col md:flex-row items-center justify-between cursor-pointer hover:scale-[1.01] transition-transform"
        @click="openGlobalChat"
      >
        <div class="space-y-2 text-center md:text-left">
          <h3 class="text-2xl font-bold">🤖 나만의 AI 금융 비서에게 물어보세요!</h3>
          <p class="opacity-90">"내 연봉에 맞는 적금 추천해줘" 라고 질문하면 AI가 분석해드립니다.</p>
        </div>
        <button class="mt-4 md:mt-0 bg-white text-indigo-700 font-bold py-3 px-6 rounded-full shadow-md hover:bg-gray-100 transition-colors">
          AI와 대화하기 →
        </button>
      </div>

      <HomeFeatures />

      <HomeSavingsCalculator />

      <section v-if="authStore.isLoggedIn" class="space-y-10 animate-in slide-in-from-bottom-10 duration-700">
        <div class="text-center md:text-left px-2">
          <h3 class="text-3xl font-black text-slate-900 tracking-tight">
            <span class="text-indigo-600">{{ userNickname }}</span>님을 위한 맞춤 추천 🎁
          </h3>
          <p class="text-slate-500 mt-3 font-bold">
            {{ recommendMessage }}
          </p>
        </div>

        <div class="bg-white rounded-[3.5rem] p-10 shadow-xl border border-indigo-50/50 space-y-12">
          
          <div>
            <h4 class="text-xl font-bold text-slate-700 mb-6 flex items-center gap-2">
              <span class="bg-indigo-100 text-indigo-600 py-1 px-3 rounded-full text-xs">예금</span>
              추천 상품
            </h4>
            <HomeRecommend
              :items="depositItems"
              message="안전하게 목돈을 굴리기 좋은 상품입니다."
              :isLoading="loading"
              @select="(item) => openDetail(item, 'deposit')"
            />
            <p v-if="!loading && depositItems.length === 0" class="text-center text-slate-400 py-4 text-sm">
              추천 가능한 예금 상품이 없습니다.
            </p>
          </div>

          <hr class="border-slate-100">

          <div>
            <h4 class="text-xl font-bold text-slate-700 mb-6 flex items-center gap-2">
              <span class="bg-purple-100 text-purple-600 py-1 px-3 rounded-full text-xs">적금</span>
              추천 상품
            </h4>
            <HomeRecommend
              :items="savingItems"
              message="매달 꾸준히 모아 자산을 불려보세요."
              :isLoading="loading"
              @select="(item) => openDetail(item, 'saving')"
            />
            
            <p v-if="!loading && savingItems.length === 0" class="mt-6 text-center text-slate-400 font-bold text-sm bg-slate-50 p-6 rounded-2xl">
              😥 추천 데이터가 부족해요. <br>
              <span class="text-indigo-500 cursor-pointer hover:underline" @click="router.push({ name: 'mypage' })">마이페이지</span>에서 정보를 업데이트해보세요!
            </p>
          </div>

        </div> 
      </section>

      <HomeLoginBanner v-else />

    </main>

    <DepositDetailModal
      :is-open="showModal"
      :product="selectedItem"
      :type="modalType"
      @close="showModal = false"
    />
  </div>
</template>