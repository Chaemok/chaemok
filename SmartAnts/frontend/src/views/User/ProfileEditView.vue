<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api' // 🐜 axios 대신 우리가 만든 api 인스턴스 사용
import ProfileEditForm from '@/components/profile/ProfileEditForm.vue' 
import SecurityModal from '@/components/auth/SecurityModal.vue' // 🐜 모달 import 필수

const authStore = useAuthStore()
const router = useRouter()

// 보안 관련 상태
const isVerified = ref(false)
const showModal = ref(true)

// 🐜 1. 비밀번호 확인 핸들러
const handleVerify = async (password) => {
  const isValid = await authStore.verifyPassword(password)
  
  if (isValid) {
    isVerified.value = true
    showModal.value = false 
  } else {
    alert('비밀번호가 일치하지 않습니다. 🐜')
  }
}

// 🐜 2. 프로필 수정 요청 함수
const handleUpdate = async (formData) => {
  try {
    // 🚨 기존 코드의 URL 에러 해결
    // api.patch를 쓰면 baseURL이 자동 적용되어 'undefined/...' 에러가 사라집니다.
    const res = await api.patch('accounts/user/', formData)
    
    // 스토어 정보 갱신
    authStore.user = res.data
    
    alert('프로필이 성공적으로 수정되었습니다! 🐜')
    router.push({ name: 'mypage' }) 

  } catch (err) {
    console.error(err)
    const errorMsg = err.response?.data?.message || '수정 중 오류가 발생했습니다.'
    alert(`수정 실패: ${errorMsg}`)
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto py-12 px-4">
    
    <SecurityModal 
      :isOpen="showModal" 
      @close="router.push({ name: 'mypage' })" 
      @confirm="handleVerify" 
    />

    <div v-if="isVerified" class="animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-black text-slate-900">프로필 수정 ✏️</h1>
        <button @click="$router.back()" class="text-sm font-bold text-slate-400 hover:text-slate-600">
          취소
        </button>
      </div>

      <div class="bg-white rounded-[2rem] shadow-xl border border-slate-100 p-8 md:p-10">
        <ProfileEditForm 
          :initialData="authStore.user" 
          @submit="handleUpdate" 
        />
      </div>
    </div>
  </div>
</template>