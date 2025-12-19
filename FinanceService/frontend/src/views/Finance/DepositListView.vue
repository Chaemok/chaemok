<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useFinanceStore } from '@/stores/finance'

// 🐜 컴포넌트 구조화 (Hana-Free 스타일)
import DepositFilter from '@/components/deposit/DepositFilter.vue'
import DepositProductCard from '@/components/deposit/DepositProductCard.vue'
import DepositDetailModal from '@/components/deposit/DepositDetailModal.vue'
import BasePagination from '@/components/common/BasePagination.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const store = useFinanceStore()

// -- 상태 관리 --
const isLoading = ref(true)
const selectedType = ref('deposit') 
const selectedSector = ref('all') // 전체, 1금융, 2금융
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
    // 🐜 [동기화] 스토어에 새로 만든 함수들 호출
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

// -- 1. 데이터 소스 결정 --
const currentSourceProducts = computed(() => {
  // selectedType이 'deposit'이면 store.depositProducts를, 아니면 savingProducts를 사용
  return selectedType.value === 'deposit' 
    ? (store.depositProducts || []) 
    : (store.savingProducts || [])
})

// -- 2. 은행 목록 동적 추출 --
const bankNames = computed(() => {
  let source = currentSourceProducts.value
  
  // 1) 금융권 필터링
  if (selectedSector.value === 'bank') {
    source = source.filter(p => !p.kor_co_nm.includes('저축은행'))
  } else if (selectedSector.value === 'savings') {
    source = source.filter(p => p.kor_co_nm.includes('저축은행'))
  }
  
  // 2) 중복을 제거한 은행 이름들을 배열로 변환
  const namesArray = Array.from(new Set(source.map(p => p.kor_co_nm)))
  
  // 3) 은행 이름들만 '먼저' 가나다순으로 정렬 (sort는 원본을 변경함)
  namesArray.sort()
  
  // 4) [중요] 정렬된 리스트 맨 앞에 '전체'를 수동으로 삽입
  return ['전체', ...namesArray]
})

// -- 3. 필터링 및 정렬 로직 --
const finalProducts = computed(() => {
  let result = currentSourceProducts.value

  // 금융권 필터
  if (selectedSector.value === 'bank') result = result.filter(p => !p.kor_co_nm.includes('저축은행'))
  else if (selectedSector.value === 'savings') result = result.filter(p => p.kor_co_nm.includes('저축은행'))

  // 은행 필터
  if (selectedBank.value !== '전체') result = result.filter(p => p.kor_co_nm === selectedBank.value)

  // 검색 필터
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(p => 
      p.fin_prdt_nm.toLowerCase().includes(query) || 
      p.kor_co_nm.toLowerCase().includes(query)
    )
  }

  // 정렬 (금리순/이름순)
  return [...result].sort((a, b) => {
    if (sortBy.value === 'rate') return (b.max_intr_rate || 0) - (a.max_intr_rate || 0)
    return a.fin_prdt_nm.localeCompare(b.fin_prdt_nm)
  })
})

// -- 4. 페이지네이션 계산 --
const totalPages = computed(() => Math.ceil(finalProducts.value.length / itemsPerPage))
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return finalProducts.value.slice(start, start + itemsPerPage)
})

const handlePageChange = (page) => {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 필터 변경 시 1페이지로 리셋
watch([selectedType, selectedSector, selectedBank, searchQuery, sortBy], () => {
  currentPage.value = 1
})

// -- 모달 핸들러 --
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
  <div class="min-h-screen bg-slate-50 pb-20">
    <div class="max-w-7xl mx-auto px-4 py-12 space-y-10">
      
      <PageHeader 
        title="예적금 상품 조회" 
        subtitle="채목님에게 딱 맞는 최고의 금리 상품을 찾아보세요. 🐜" 
      />

      <div class="flex justify-center">
        <div class="flex bg-slate-200/50 p-1.5 rounded-[2rem] w-full max-w-sm">
          <button @click="selectedType = 'deposit'"
                  :class="selectedType === 'deposit' ? 'bg-white text-primary shadow-md' : 'text-slate-500'"
                  class="flex-1 py-3 text-lg font-black rounded-[1.8rem] transition-all">
            예금
          </button>
          <button @click="selectedType = 'saving'"
                  :class="selectedType === 'saving' ? 'bg-white text-primary shadow-md' : 'text-slate-500'"
                  class="flex-1 py-3 text-lg font-black rounded-[1.8rem] transition-all">
            적금
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
        <span class="loading loading-spinner loading-lg text-primary"></span>
        <p class="mt-4 text-slate-400 font-bold">금융 상품 정보를 분석 중입니다... 🐜</p>
      </div>

      <div v-else class="animate-fade-in-up space-y-10">
        <DepositFilter 
          v-model:sector="selectedSector"
          v-model:bank="selectedBank"
          v-model:query="searchQuery"
          v-model:sort="sortBy"
          :bankNames="bankNames"
        />

        <EmptyState v-if="finalProducts.length === 0" />

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <DepositProductCard 
            v-for="product in paginatedProducts" 
            :key="product.id"
            :product="product"
            @click="openDetailModal(product)"
          />
        </div>

        <BasePagination 
          v-if="totalPages > 1"
          :current-page="currentPage"
          :total-pages="totalPages"
          @page-change="handlePageChange"
        />
      </div>
    </div>

    <DepositDetailModal 
      v-if="selectedProduct"
      :product="selectedProduct"
      :is-open="isModalOpen"
      @close="closeDetailModal"
    />
  </div>
</template>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out forwards;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>