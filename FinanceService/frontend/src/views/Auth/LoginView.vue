<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import LoginForm from '@/components/auth/LoginForm.vue'

const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async (credentials) => {
  const success = await authStore.login(credentials)
  if (success) router.push('/')
}
</script>

<template>
  <AuthLayout>
    <template #title>개미들의 투자 커뮤니티 로그인</template>
    <template #form>
      <LoginForm @submit="handleLogin" />
      <p class="mt-8 text-center text-sm text-slate-400 font-medium">
        계정이 없으신가요? 
        <router-link to="/signup" class="text-primary font-bold hover:underline">회원가입</router-link>
      </p>
    </template>
  </AuthLayout>
</template>