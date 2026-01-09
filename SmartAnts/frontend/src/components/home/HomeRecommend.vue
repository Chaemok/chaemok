<script setup>
import { useAuthStore } from '@/stores/auth'
// import { useRouter } from 'vue-router' // ❌ 삭제: 페이지 이동 안 함

const props = defineProps({
  items: Array,
  message: String,
  isLoading: Boolean
})

// ✅ 추가: 부모에게 이벤트를 보내기 위한 설정
const emit = defineEmits(['select'])

const authStore = useAuthStore()
// const router = useRouter() // ❌ 삭제

// ✅ 수정: 클릭 시 페이지 이동 대신 'select' 이벤트 발생
const handleClick = (item) => {
  emit('select', item)
}
</script>

<template>
  <section>
    <div class="flex items-center justify-between mb-8">
      <h3 class="text-2xl font-black text-slate-800">
        {{ authStore.user?.nickname || '회원' }}님을 위한 분석 결과 💎
      </h3>
      <router-link to="/deposit" class="text-sm font-bold text-blue-600">전체 상품보기</router-link>
    </div>

    <div v-if="items?.length > 0" class="mb-8 p-6 bg-blue-50/50 rounded-3xl border border-blue-100 flex items-start gap-4">
      <span class="text-2xl">💡</span>
      <p class="text-sm font-bold text-blue-800/80 leading-relaxed">{{ message }}</p>
    </div>
    
    <div v-if="!isLoading" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="(item, idx) in items" :key="idx" 
           @click="handleClick(item)"
           class="group flex bg-white shadow-sm border border-slate-100 rounded-[2.5rem] hover:shadow-xl hover:border-blue-200 transition-all cursor-pointer overflow-hidden">
        <div class="w-1/3 bg-slate-50 flex flex-col items-center justify-center border-r border-slate-50">
          <span class="text-3xl mb-2">🏛️</span>
          <span class="text-[10px] font-black text-slate-400 uppercase tracking-tighter">Rank {{ idx + 1 }}</span>
        </div>
        <div class="p-8 flex-1">
          <div class="text-[10px] font-bold text-blue-500 mb-1">
            {{ item.product?.kor_co_nm || item.kor_co_nm }}
          </div>
          <h2 class="text-lg font-black text-slate-800 mb-4 group-hover:text-blue-600 transition-colors">
            {{ item.product?.fin_prdt_nm || item.fin_prdt_nm }}
          </h2>
          <div class="flex items-baseline gap-1">
            <span class="text-xs text-slate-400 font-bold">최고 연</span>
            <span class="text-2xl font-black text-blue-600">{{ item.intr_rate2 }}%</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="i in 2" :key="i" class="h-40 bg-slate-100 rounded-[2.5rem] animate-pulse"></div>
    </div>
  </section>
</template>