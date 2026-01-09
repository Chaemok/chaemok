<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useFinanceStore } from '@/stores/finance'

import DepositFilter from '@/components/deposit/DepositFilter.vue'
import DepositProductCard from '@/components/deposit/DepositProductCard.vue'
import DepositDetailModal from '@/components/deposit/DepositDetailModal.vue'
import BasePagination from '@/components/common/BasePagination.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/BaseEmpty.vue'

const store = useFinanceStore()

const isLoading = ref(true)
const selectedType = ref('deposit') 
const selectedSector = ref('all') 
const selectedBank = ref('전체')
const searchQuery = ref('')
const sortBy = ref('rate')

const currentPage = ref(1)
const itemsPerPage = 12

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

const currentSourceProducts = computed(() => {
  return selectedType.value === 'deposit' 
    ? (store.depositProducts || []) 
    : (store.savingProducts || [])
})

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
  <div class="min-h-screen bg-slate-50 font-pretendard">
    <PageHeader 
      title="Deposits/Savings Products" 
      subtitle="나에게 딱 맞는 최고 금리 예적금 상품을 비교해보세요."
      bgClass="bg-blue-900" 
    />

    <div class="max-w-7xl mx-auto px-4 pb-20 -mt-8 relative z-20">
      
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-40">
        <span class="loading loading-spinner loading-lg text-blue-600"></span>
        <p class="mt-6 text-slate-400 font-bold animate-pulse">최적의 상품을 분석하고 있습니다... 🐜</p>
      </div>

      <div v-else class="animate-in fade-in slide-in-from-bottom-4 duration-700 space-y-8">
        
        <div class="bg-white rounded-[2.5rem] p-6 md:p-10 shadow-xl shadow-slate-200/50 border border-white">
          <DepositFilter 
            v-model:type="selectedType" 
            v-model:sector="selectedSector"
            v-model:bank="selectedBank"
            v-model:query="searchQuery"
            v-model:sort="sortBy"
            :bankNames="bankNames"
          />
        </div>

        <div class="flex items-center justify-between px-4">
          <div class="flex items-center gap-2">
            <span class="text-slate-800 font-black text-xl">검색 결과</span>
            <span class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-black">{{ finalProducts.length }}건</span>
          </div>
          <span class="text-[11px] text-slate-400 font-bold tracking-tight">* 금리는 세전 기준입니다.</span>
        </div>

        <EmptyState v-if="finalProducts.length === 0" />

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <DepositProductCard 
            v-for="product in paginatedProducts" 
            :key="product.id"
            :product="product"
            @click="openDetailModal(product)"
            class="hover:-translate-y-2 hover:shadow-2xl transition-all duration-300"
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
.font-pretendard { font-family: 'Pretendard', sans-serif; }
</style>  