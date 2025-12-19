<script setup>
import { RouterLink } from 'vue-router'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
</script>

<template>
  <div class="max-w-xl mx-auto mt-20 px-4 text-center">
    <BaseCard>
      <div class="py-10">
        <div class="text-6xl mb-6">🎉</div>
        <h1 class="text-3xl font-bold text-gray-900 mb-4">회원가입을 축하합니다!</h1>
        <p class="text-gray-600 mb-8">
          성공적으로 가입되었으며, <br />
          <span class="font-bold text-blue-600">자동으로 로그인</span> 되었습니다.
        </p>
        
        <RouterLink :to="{ name: 'home' }">
          <BaseButton color="blue" class="w-full py-3 text-lg">
            메인으로 이동하기
          </BaseButton>
        </RouterLink>
      </div>
    </BaseCard>
  </div>
</template>