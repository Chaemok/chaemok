<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AuthLayout from '@/components/auth/AuthLayout.vue'
import SignupForm from '@/components/auth/SignupForm.vue'

const router = useRouter()
const authStore = useAuthStore()

const handleSignup = async (userData) => {
  const success = await authStore.signup(userData)
  if (success) router.push('/login')
}
</script>

<template>
  <AuthLayout>
    <template #title>새로운 개미가 되어보세요 🐜</template>
    <template #form>
      <SignupForm @submit="handleSignup" />
      <p class="mt-8 text-center text-sm text-slate-400 font-medium">
        이미 계정이 있나요? 
        <router-link to="/login" class="text-primary font-bold hover:underline">로그인</router-link>
      </p>
    </template>
  </AuthLayout>
</template>