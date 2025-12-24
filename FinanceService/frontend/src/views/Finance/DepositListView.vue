<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useFinanceStore } from '@/stores/finance'

// 컴포넌트 임포트
import DepositFilter from '@/components/deposit/DepositFilter.vue'
import DepositProductCard from '@/components/deposit/DepositProductCard.vue'
import DepositDetailModal from '@/components/deposit/DepositDetailModal.vue'
import BasePagination from '@/components/common/BasePagination.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/BaseEmpty.vue'

const store = useFinanceStore()

// -- 상태 관리 --
const isLoading = ref(true)
const selectedType = ref('deposit') 
const selectedSector = ref('all') 
const selectedBank = ref('전체')
const searchQuery = ref('')
const sortBy = ref('rate')

// 페이지네이션
const currentPage = ref(1)
const itemsPerPage = 12

// 모달 상태
const isModalOpen = ref(false)
const selectedProduct = ref(null)

onMounted(async () => {
  try {
    isLoading.value = true
    await Promise.all([
      store.getDepositProducts(), 
      store.getSavingProducts()
    ])
  } catch (err) {
    console.error('데이터 로딩 중 에러:', err)
  } finally {
    isLoading.value = false
  }
})

// -- 데이터 소스 결정 --
const currentSourceProducts = computed(() => {
  return selectedType.value === 'deposit' 
    ? (store.depositProducts || []) 
    : (store.savingProducts || [])
})

// -- 은행 목록 동적 추출 --
const bankNames = computed(() => {
  let source = currentSourceProducts.value
  if (selectedSector.value === 'bank') {
    source = source.filter(p => !p.kor_co_nm.includes('저축은행'))
  } else if (selectedSector.value === 'savings') {
    source = source.filter(p => p.kor_co_nm.includes('저축은행'))
  }
  const namesArray = Array.from(new Set(source.map(p => p.kor_co_nm)))
  namesArray.sort()
  return ['전체', ...namesArray]
})

// -- 필터링 및 정렬 로직 --
const finalProducts = computed(() => {
  let result = currentSourceProducts.value
  if (selectedSector.value === 'bank') result = result.filter(p => !p.kor_co_nm.includes('저축은행'))
  else if (selectedSector.value === 'savings') result = result.filter(p => p.kor_co_nm.includes('저축은행'))
  if (selectedBank.value !== '전체') result = result.filter(p => p.kor_co_nm === selectedBank.value)
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(p => 
      p.fin_prdt_nm.toLowerCase().includes(query) || 
      p.kor_co_nm.toLowerCase().includes(query)
    )
  }
  return [...result].sort((a, b) => {
    if (sortBy.value === 'rate') return (b.max_intr_rate || 0) - (a.max_intr_rate || 0)
    return a.fin_prdt_nm.localeCompare(b.fin_prdt_nm)
  })
})

// -- 페이지네이션 계산 --
const totalPages = computed(() => Math.ceil(finalProducts.value.length / itemsPerPage))
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return finalProducts.value.slice(start, start + itemsPerPage)
})

const handlePageChange = (page) => {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

watch([selectedType, selectedSector, selectedBank, searchQuery, sortBy], () => {
  currentPage.value = 1
})

// 모달 핸들러
const openDetailModal = (product) => {
  selectedProduct.value = product
  isModalOpen.value = true
}

const closeDetailModal = () => {
  isModalOpen.value = false
  selectedProduct.value = null
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 pb-32 font-pretendard relative overflow-hidden">
    
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-blue-100/60 blur-[120px] rounded-full pointer-events-none z-0"></div>

    <div class="max-w-7xl mx-auto px-6 pt-20 relative z-10">
      
      <div class="text-center mb-10 space-y-3">
        <h1 class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight leading-tight">
          나에게 딱 맞는 <br class="md:hidden" />
          <span class="text-blue-600 inline-block relative">
            최고의 상품
            <svg class="absolute -bottom-2 left-0 w-full h-3 text-blue-200 -z-10 opacity-60" viewBox="0 0 100 10" preserveAspectRatio="none">
              <path d="M0 5 Q 50 10 100 5" stroke="currentColor" stroke-width="8" fill="none" />
            </svg>
          </span> 찾기
        </h1>
        <p class="text-slate-500 text-lg font-medium">예금부터 적금까지, 스마트 앤츠가 분석해드려요 🐜</p>
      </div>

      <div class="flex justify-center mb-14">
        <div class="bg-white p-1.5 rounded-full shadow-[0_4px_20px_rgba(0,0,0,0.05)] border border-slate-100 w-full max-w-[340px] flex">
          <button @click="selectedType = 'deposit'"
                  class="flex-1 py-3 text-[16px] font-bold rounded-full transition-all duration-300 flex items-center justify-center gap-2"
                  :class="selectedType === 'deposit' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-400 hover:bg-slate-50 hover:text-slate-600'">
            <span>💰 정기예금</span>
          </button>
          
          <button @click="selectedType = 'saving'"
                  class="flex-1 py-3 text-[16px] font-bold rounded-full transition-all duration-300 flex items-center justify-center gap-2"
                  :class="selectedType === 'saving' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-400 hover:bg-slate-50 hover:text-slate-600'">
            <span>🌱 정기적금</span>
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-40">
        <div class="loading loading-spinner loading-lg text-blue-600"></div>
        <p class="mt-6 text-slate-400 font-bold animate-pulse">최적의 상품을 분석하고 있어요...</p>
      </div>

      <div v-else class="animate-fade-in-up space-y-8">
        
        <div class="bg-white rounded-[2rem] p-6 md:p-8 shadow-xl shadow-slate-200/40 border border-slate-100">
          <DepositFilter 
            v-model:sector="selectedSector"
            v-model:bank="selectedBank"
            v-model:query="searchQuery"
            v-model:sort="sortBy"
            :bankNames="bankNames"
          />
        </div>

        <div class="flex items-center justify-between px-2">
          <div class="flex items-center gap-2">
            <span class="text-slate-800 font-bold text-lg">검색 결과</span>
            <span class="bg-blue-100 text-blue-700 px-3 py-0.5 rounded-full text-sm font-black">{{ finalProducts.length }}건</span>
          </div>
          <span class="text-xs text-slate-400 font-medium tracking-tight">* 금리는 세전 기준입니다.</span>
        </div>

        <EmptyState v-if="finalProducts.length === 0" />

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <DepositProductCard 
            v-for="product in paginatedProducts" 
            :key="product.id"
            :product="product"
            @click="openDetailModal(product)"
            class="hover:-translate-y-1 hover:shadow-lg transition-all duration-300 border border-slate-100"
          />
        </div>

        <div class="pt-8">
          <BasePagination 
            v-if="totalPages > 1"
            :current-page="currentPage"
            :total-pages="totalPages"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>

    <DepositDetailModal 
      :is-open="isModalOpen"
      :product="selectedProduct"
      @close="closeDetailModal"
    />
  </div>
</template>

<style scoped>
/* 폰트 적용 */
.font-pretendard { font-family: 'Pretendard', sans-serif; }

/* 애니메이션 */
.animate-fade-in-up { animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>