<script setup>
import { onMounted, ref, computed } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import api from '@/api'
import FinanceCard from '@/components/finance/FinanceCard.vue'
import FinanceDetailModal from '@/components/finance/FinanceDetailModal.vue'

const store = useFinanceStore()
const searchQuery = ref('')

// 모달 제어 상태
const isModalOpen = ref(false)
const selectedProduct = ref(null)

// 🔍 실시간 필터링 리스트
const filteredProducts = computed(() => {
  return store.allProducts.filter(p => 
    p.fin_prdt_nm.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
    p.kor_co_nm.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 🏛️ 상세 모달 열기
const openDetail = (product) => {
  selectedProduct.value = product
  isModalOpen.value = true
}

// 🐜 가입하기 로직 (백엔드 연동)
const handleJoinProduct = async (optionPk) => {
  try {
    const res = await api.post(`finlife/deposits/join/${optionPk}/`)
    alert(res.data.message)
    // 가입 성공 후 모달 닫기 (선택사항)
    // isModalOpen.value = false
  } catch (err) {
    console.error('가입 실패:', err)
    alert('상품 가입 중 오류가 발생했습니다.')
  }
}

onMounted(() => {
  store.fetchProducts()
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-8 space-y-10">
    <header class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <h2 class="text-4xl font-black text-slate-800 tracking-tight">금융 상품 탐색 🐜</h2>
        <p class="text-slate-400 font-medium">Smart Ants가 분석한 전국 은행의 최적 금리 상품들입니다.</p>
      </div>
      
      <div class="tabs tabs-boxed bg-slate-200/50 p-1.5 rounded-2xl">
        <button 
          @click="store.setProductType('deposits')" 
          :class="{ 'bg-white shadow-md text-primary': store.productType === 'deposits' }"
          class="tab font-bold transition-all px-10 py-2 rounded-xl h-auto"
        >정기예금</button>
        <button 
          @click="store.setProductType('savings')" 
          :class="{ 'bg-white shadow-md text-primary': store.productType === 'savings' }"
          class="tab font-bold transition-all px-10 py-2 rounded-xl h-auto"
        >정기적금</button>
      </div>
    </header>

    <div class="relative max-w-2xl">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="어떤 은행이나 상품을 찾으시나요?" 
        class="input input-lg w-full rounded-[1.5rem] border-slate-200 focus:border-primary focus:ring-4 focus:ring-primary/10 pl-14 text-lg" 
      />
      <span class="absolute left-5 top-1/2 -translate-y-1/2 text-2xl">🔍</span>
    </div>

    <div v-if="store.isMainLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="n in 6" :key="n" class="h-56 bg-white border border-slate-100 animate-pulse rounded-[2rem]"></div>
    </div>
    
    <div v-else-if="filteredProducts.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <FinanceCard 
        v-for="product in filteredProducts" 
        :key="product.id" 
        :product="product"
        @click="openDetail(product)" 
      />
    </div>

    <div v-else class="flex flex-col items-center justify-center py-32 space-y-4">
      <div class="text-7xl">🐜💨</div>
      <div class="text-center">
        <p class="text-xl font-bold text-slate-700">검색 결과가 없어요</p>
        <p class="text-slate-400">다른 키워드로 다시 검색해보시겠어요?</p>
      </div>
      <button @click="searchQuery = ''" class="btn btn-ghost text-primary">검색 초기화</button>
    </div>

    <FinanceDetailModal 
      v-if="selectedProduct"
      :product="selectedProduct" 
      :isOpen="isModalOpen"
      @close="isModalOpen = false"
      @join="handleJoinProduct"
    />
  </div>
</template>