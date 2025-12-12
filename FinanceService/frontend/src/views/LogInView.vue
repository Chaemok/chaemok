<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user' 
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'

const store = useUserStore()
const username = ref('')
const password = ref('')

const handleLogin = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  // [수정 3] auth.js에 정의한 함수 이름(login) 호출
  store.logIn(payload)
}
</script>

<template>
  <div class="max-w-md mx-auto mt-16 px-4">
    <BaseCard>
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-gray-900">로그인</h1>
        <p class="text-gray-500 text-sm mt-2">서비스 이용을 위해 로그인해주세요.</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2">아이디</label>
          <input 
            type="text" 
            v-model="username" 
            placeholder="아이디" 
            class="input input-bordered w-full bg-gray-50 focus:bg-white" 
            required 
          />
        </div>
        
        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2">비밀번호</label>
          <input 
            type="password" 
            v-model="password" 
            placeholder="비밀번호" 
            class="input input-bordered w-full bg-gray-50 focus:bg-white" 
            required 
          />
        </div>

        <div class="flex items-center justify-between">
          <label class="cursor-pointer label">
            <input type="checkbox" class="checkbox checkbox-xs checkbox-primary mr-2" />
            <span class="label-text text-gray-600">로그인 상태 유지</span>
          </label>
          <a href="#" class="text-sm text-blue-600 hover:underline">비밀번호 찾기</a>
        </div>

        <BaseButton type="submit" color="blue" class="w-full py-3 text-lg">
          로그인하기
        </BaseButton>
      </form>

      <div class="mt-6 text-center text-sm text-gray-500">
        아직 회원이 아니신가요? 
        <RouterLink :to="{ name: 'signup' }" class="text-blue-600 font-bold hover:underline">
          회원가입
        </RouterLink>
      </div>
    </BaseCard>
  </div>
</template>