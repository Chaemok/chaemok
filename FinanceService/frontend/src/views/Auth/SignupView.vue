<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import SignupForm from '@/components/auth/SignupForm.vue'
import WelcomeModal from '@/components/auth/WelcomeModal.vue' // 🐜 컴포넌트 호출

const router = useRouter()
const authStore = useAuthStore()
const showWelcomeModal = ref(false)

const handleSignup = async (userData) => {
  try {
    // 🐜 가입과 동시에 스토어에서 자동으로 토큰 저장(로그인)이 일어남
    await authStore.signup(userData)
    showWelcomeModal.value = true
  } catch (err) {
    console.error('가입 실패:', err)
  }
}

const goToHome = () => {
  showWelcomeModal.value = false
  router.push({ name: 'home' })
}
</script>

<template>
  <AuthLayout>
    <template #title>새로운 개미가 되어보세요 🐜</template>
    <template #form>
      <SignupForm @submit="handleSignup" />
    </template>
  </AuthLayout>

  <WelcomeModal :isOpen="showWelcomeModal" @confirm="goToHome" />
</template>