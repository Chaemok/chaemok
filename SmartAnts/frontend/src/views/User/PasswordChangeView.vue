<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import PasswordChangeForm from '@/components/profile/PasswordChangeForm.vue'

const router = useRouter()
const authStore = useAuthStore()

const handleChangePassword = async (formData) => {
  try {
    // 🐜 [중요] dj-rest-auth가 요구하는 정확한 필드명으로 전송
    const payload = {
      old_password: formData.old_password,      // 현재 비밀번호
      new_password1: formData.new_password,     // 새 비밀번호
      new_password2: formData.confirm_password  // 새 비밀번호 확인
    }
    
    // API 호출
    await api.post('accounts/password/change/', payload)
    
    alert('✅ 비밀번호가 변경되었습니다. 보안을 위해 다시 로그인해주세요.')
    authStore.logout() 
    router.push('/login')
    
  } catch (err) {
    console.error('비밀번호 변경 에러 상세:', err.response?.data) // 👈 여기서 F12 눌러서 에러 내용 확인 가능

    // 400 에러 처리 (상황별 안내)
    const errorData = err.response?.data
    
    if (errorData?.old_password) {
      alert(`❌ 현재 비밀번호가 일치하지 않습니다.\n(${errorData.old_password[0]})`)
    } 
    else if (errorData?.new_password1) {
      // 비밀번호가 너무 짧거나, 숫자가 없거나 하는 등의 유효성 검사 실패
      alert(`❌ 새 비밀번호를 사용할 수 없습니다.\n(${errorData.new_password1[0]})`)
    } 
    else if (errorData?.non_field_errors) {
      alert(`❌ 오류: ${errorData.non_field_errors[0]}`)
    } 
    else {
      alert('비밀번호 변경에 실패했습니다. 입력값을 다시 확인해주세요.')
    }
  }
}
</script>

<template>
  <AuthLayout>
    <template #title>비밀번호 변경 🔑</template>
    <template #form>
      <PasswordChangeForm @submit="handleChangePassword" />
      <button @click="router.back()" class="w-full py-4 mt-2 text-slate-400 font-bold hover:text-slate-600 transition-colors">
        취소하고 돌아가기
      </button>
    </template>
  </AuthLayout>
</template>