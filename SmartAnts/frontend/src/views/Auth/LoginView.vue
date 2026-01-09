<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import LoginForm from '@/components/auth/LoginForm.vue'

const router = useRouter()
const authStore = useAuthStore()

// LoginForm에서 emit('submit', {username, password})한 값을 받음
const handleLogin = async (credentials) => {
  try {
    // 1. 스토어 로그인 액션 실행 (에러나면 catch로 넘어감)
    await authStore.login(credentials)
    
    // 2. 성공 시 홈으로 이동 (replace는 뒤로가기 방지)
    router.replace({ name: 'home' }) 
    
  } catch (err) {
    // 3. 실패 시 알림
    console.error(err)
    alert('로그인 실패! 아이디와 비밀번호를 확인해주세요.')
  }
}
</script>

<template>
  <AuthLayout>
    <template #title>개미들의 투자 커뮤니티 로그인 🐜</template>
    
    <template #form>
      <LoginForm @submit="handleLogin" />
      
      <p class="mt-8 text-center text-sm text-slate-400 font-medium">
        계정이 없으신가요? 
        <router-link :to="{ name: 'signup' }" class="text-blue-600 font-bold hover:underline ml-1">
          회원가입
        </router-link>
      </p>
    </template>
  </AuthLayout>
</template>