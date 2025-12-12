<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios'
import { useFinanceStore } from '@/stores/finance'

// 부모(List)로부터 받을 데이터
const props = defineProps({
  product: Object,   // 선택된 상품 객체
  isOpen: Boolean    // 모달 표시 여부
})

// 부모에게 보낼 이벤트 (닫기)
const emit = defineEmits(['close'])

const userStore = useUserStore()
const financeStore = useFinanceStore()
const API_URL = 'http://127.0.0.1:8000'

// 가입 여부 확인
const isJoined = computed(() => {
  // userStore의 정보와 product의 contract_user 비교
  // (백엔드 Serializer에서 contract_user 필드를 보내준다고 가정)
  if (!props.product || !userStore.isLogin) return false
  return props.product.contract_user?.includes(userStore.userId)
})

// 가입하기/해지하기 기능
const joinProduct = () => {
  if (!userStore.isLogin) {
    alert('로그인이 필요합니다.')
    return
  }

  axios({
    method: 'post',
    url: `${API_URL}/api/finances/deposits/${props.product.id}/join/`,
    headers: { Authorization: `Bearer ${userStore.token}` }
  })
  .then((res) => {
    alert(res.data.message || '처리되었습니다.')
    // 데이터 갱신을 위해 스토어 액션 호출 (선택사항)
    financeStore.getDepositProducts()
  })
  .catch((err) => {
    console.error(err)
    alert('처리에 실패했습니다.')
  })
}
</script>

<template>
  <Transition name="modal">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center px-4" @click.self="$emit('close')">
      
      <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

      <div class="relative bg-white rounded-3xl shadow-2xl w-full max-w-lg overflow-hidden transform transition-all p-8">
        
        <button @click="$emit('close')" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <div class="text-center mb-8">
          <span class="inline-block bg-blue-50 text-blue-600 px-3 py-1 rounded-full text-sm font-bold mb-3">
            {{ product.bank_name }}
          </span>
          <h2 class="text-2xl font-bold text-gray-800 break-keep">
            {{ product.product_name }}
          </h2>
        </div>

        <div class="grid grid-cols-2 gap-4 mb-8 bg-gray-50 p-6 rounded-2xl">
          <div class="text-center">
            <p class="text-sm text-gray-500 mb-1">기본 금리</p>
            <p class="text-xl font-bold text-gray-700">{{ product.interest_rate }}%</p>
          </div>
          <div class="text-center border-l border-gray-200">
            <p class="text-sm text-gray-500 mb-1">최고 우대 금리</p>
            <p class="text-xl font-bold text-emerald-500">{{ product.highest_rate }}%</p>
          </div>
          <div class="col-span-2 border-t border-gray-200 pt-4 mt-2">
            <p class="text-sm text-gray-500 mb-1">가입 조건 및 기간</p>
            <p class="font-medium text-gray-700">{{ product.join_term || '제한 없음' }}</p>
          </div>
        </div>

        <div class="flex gap-3">
          <button @click="$emit('close')" class="flex-1 py-3.5 rounded-xl bg-gray-100 text-gray-700 font-bold hover:bg-gray-200 transition-colors">
            닫기
          </button>
          
          <button 
            v-if="userStore.isLogin" 
            @click="joinProduct"
            class="flex-1 py-3.5 rounded-xl font-bold text-white transition-colors shadow-lg shadow-blue-200"
            :class="isJoined ? 'bg-red-500 hover:bg-red-600' : 'bg-blue-600 hover:bg-blue-700'"
          >
            {{ isJoined ? '해지하기' : '가입하기' }}
          </button>
        </div>

      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* 모달 애니메이션 CSS */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95);
  opacity: 0;
}
.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: all 0.3s ease-out;
}
</style>