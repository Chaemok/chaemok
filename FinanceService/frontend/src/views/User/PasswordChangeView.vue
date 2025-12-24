<script setup>
import { useRouter } from 'vue-router'
import api from '@/api'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import PasswordChangeForm from '@/components/profile/PasswordChangeForm.vue'

const router = useRouter()

const handleChangePassword = async (data) => {
  try {
    await api.post('accounts/password/change/', data)
    alert('비밀번호가 변경되었습니다. 다시 로그인해주세요.')
    // 로그아웃 처리 로직 추가 가능
    router.push('/login')
  } catch (err) {
    alert('현재 비밀번호가 틀렸거나 변경에 실패했습니다.')
  }
}
</script>

<template>
  <AuthLayout>
    <template #title>비밀번호 변경</template>
    <template #form>
      <PasswordChangeForm @submit="handleChangePassword" />
      <button @click="router.back()" class="btn btn-ghost w-full mt-4 text-slate-400 font-bold">취소</button>
    </template>
  </AuthLayout>
</template>