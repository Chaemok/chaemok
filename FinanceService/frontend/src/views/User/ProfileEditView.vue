<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'
import AuthLayout from '@/components/auth/AuthLayout.vue'
import ProfileEditForm from '@/components/profile/ProfileEditForm.vue'

const router = useRouter()
const authStore = useAuthStore()

const handleUpdate = async (updatedData) => {
  try {
    await api.put('accounts/user/', updatedData) // 백엔드 경로에 맞춰 수정
    alert('정보가 성공적으로 수정되었습니다! 🐜')
    authStore.getUserInfo() // 스토어 정보 갱신
    router.push('/profile')
  } catch (err) {
    alert('수정 중 오류가 발생했습니다.')
  }
}
</script>

<template>
  <AuthLayout>
    <template #title>회원정보 수정</template>
    <template #form>
      <ProfileEditForm :initialData="authStore.user" @submit="handleUpdate" />
      <button @click="router.back()" class="btn btn-ghost w-full mt-4 text-slate-400 font-bold">취소</button>
    </template>
  </AuthLayout>
</template>