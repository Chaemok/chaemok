<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useFinanceStore } from '@/stores/finance'

// 컴포넌트 임포트
import PageHeader from '@/components/layout/PageHeader.vue'
import ProductTypeToggle from '@/components/ProductTypeToggle.vue'
import DepositFilterPanel from '@/components/DepositFilterPanel.vue'
import DepositProductCard from '@/components/DepositProductCard.vue'
import BasePagination from '@/components/BasePagination.vue'
import DepositDetailModal from '@/components/DepositDetailModal.vue'

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
const itemsPerPage = 24

// 모달
const isModalOpen = ref(false)
const selectedProduct = ref(null)

onMounted(async () => {
  try {
    // 예금, 적금 데이터 모두 가져오기
    await Promise.all([store.getDepositProducts(), store.getSavingProducts()])
  } catch (err) {
    console.error('데이터 로딩 중 일부 실패:', err)
  } finally {
    isLoading.value = false
  }
})

// -- 1. 데이터 소스 --
const currentSourceProducts = computed(() => {
  return selectedType.value === 'deposit' ? (store.depositProducts || []) : (store.savingProducts || [])
})

// -- 2. 은행 목록 추출 --
const bankNames = computed(() => {
  let source = currentSourceProducts.value
  
  if (selectedSector.value === '1') source = source.filter(p => !p.bank_name.includes('저축은행'))
  else if (selectedSector.value === '2') source = source.filter(p => p.bank_name.includes('저축은행'))
  
  const names = new Set(source.map(p => p.bank_name))
  return ['전체', ...names].sort()
})

// -- 3. 최종 필터링 및 정렬 --
const finalProducts = computed(() => {
  let result = currentSourceProducts.value || []

  // 1) 금융권 필터
  if (selectedSector.value === '1') result = result.filter(p => !p.bank_name.includes('저축은행'))
  else if (selectedSector.value === '2') result = result.filter(p => p.bank_name.includes('저축은행'))

  // 2) 은행 필터
  if (selectedBank.value !== '전체') result = result.filter(p => p.bank_name === selectedBank.value)

  // 3) 검색 필터
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(p => 
      p.product_name.toLowerCase().includes(query) || 
      p.bank_name.toLowerCase().includes(query)
    )
  }

  // 4) 정렬
  return [...result].sort((a, b) => {
    if (sortBy.value === 'rate') {
      return (b.highest_rate || 0) - (a.highest_rate || 0)
    } else {
      return a.product_name.localeCompare(b.product_name)
    }
  })
})

// -- 4. 페이지네이션 --
const totalPages = computed(() => Math.ceil(finalProducts.value.length / itemsPerPage))

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return finalProducts.value.slice(start, end)
})

const handlePageChange = (page) => {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// -- Watcher --
watch([selectedType, selectedSector, selectedBank, searchQuery, sortBy], () => {
  currentPage.value = 1
})

watch([selectedSector, selectedType], () => {
  selectedBank.value = '전체'
})

// -- 모달 핸들러 --
const openDetailModal = (id) => {
  selectedProduct.value = currentSourceProducts.value.find(p => p.id === id)
  isModalOpen.value = true
  document.body.style.overflow = 'hidden'
}

const closeDetailModal = () => {
  isModalOpen.value = false
  selectedProduct.value = null
  document.body.style.overflow = ''
}
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-8 min-h-screen bg-gray-50">
    
    <PageHeader 
      title="💰 금융 상품 조회" 
      subtitle="예금과 적금, 나에게 맞는 최고의 상품을 찾아보세요." 
    />

    <ProductTypeToggle v-model="selectedType" />

    <div v-if="isLoading" class="flex flex-col items-center justify-center py-20">
      <span class="loading loading-spinner loading-lg text-primary"></span>
      <p class="mt-4 text-gray-500 font-medium">최신 금융 상품 정보를 불러오는 중...</p>
    </div>

    <div v-else class="animate-fade-in-up">
      
      <DepositFilterPanel 
        v-model:sector="selectedSector"
        v-model:bank="selectedBank"
        v-model:query="searchQuery"
        v-model:sort="sortBy"
        :bankNames="bankNames"
      />

      <div class="flex justify-between items-end mb-4 px-2">
        <h2 class="text-xl font-bold text-gray-800">
          <span class="text-blue-600 mr-1">{{ selectedType === 'deposit' ? '예금' : '적금' }}</span>
          검색 결과 <span class="text-gray-800">{{ finalProducts.length }}</span>건
          <span class="text-sm font-normal text-gray-500 ml-2" v-if="totalPages > 0">
            (페이지 {{ currentPage }} / {{ totalPages }})
          </span>
        </h2>
        <span class="text-xs text-gray-400">*최고 우대금리 기준 (세전)</span>
      </div>

      <div v-if="finalProducts.length === 0" class="text-center py-20 bg-white rounded-2xl border border-dashed border-gray-300">
        <p class="text-4xl mb-4">😢</p>
        <p class="text-xl text-gray-400 font-bold">조건에 맞는 상품이 없습니다.</p>
        <p class="text-gray-400 mt-2">검색 조건을 변경해보세요.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-12">
        <DepositProductCard 
          v-for="product in paginatedProducts" 
          :key="product.id"
          :product="product"
          @click-card="openDetailModal"
        />
      </div>

      <BasePagination 
        v-if="totalPages > 1"
        :current-page="currentPage"
        :total-pages="totalPages"
        @page-change="handlePageChange"
      />
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

/* 👇 여기가 문제였습니다. 괄호가 제대로 닫혀야 합니다. */
@keyframes fadeInUp {
  from { 
    opacity: 0; 
    transform: translateY(20px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}
</style>