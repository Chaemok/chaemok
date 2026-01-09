<script setup>
import { ref, onMounted, provide } from 'vue' // ✅ provide 추가
import { RouterView, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import TheFooter from '@/components/layout/TheFooter.vue'
import DefaultLayout from '@/components/layout/DefaultLayout.vue'
import SplashScreen from '@/components/common/SplashScreen.vue' 
import GlobalChatBot from '@/components/common/GlobalChatBot.vue'

const route = useRoute()
const authStore = useAuthStore()
const isLoading = ref(true)

// ✅ 챗봇 제어용 Ref 생성
const globalChatBotRef = ref(null)

// ✅ [핵심] 하위 컴포넌트(HomeView 등)에서 챗봇을 열 수 있게 함수 제공
const openGlobalChat = () => {
  if (globalChatBotRef.value) {
    globalChatBotRef.value.openChat()
  }
}
provide('openGlobalChat', openGlobalChat) 


onMounted(() => {
  // ✅ 새로고침 시 로그인 상태 복구 (Store 액션 사용)
  authStore.initialize()

  setTimeout(() => {
    isLoading.value = false
  }, 1500)
})
</script>

<template>
  <transition name="splash-fade">
    <SplashScreen v-if="isLoading" />
  </transition>
  
  <div v-if="!isLoading" class="min-h-screen flex flex-col font-pretendard relative">
    
    <DefaultLayout>
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </transition>
      </RouterView>
    </DefaultLayout>

    <TheFooter />
    
    <GlobalChatBot ref="globalChatBotRef" />
  </div>
</template>

<style>
/* 기존 스타일 유지 */
.font-pretendard { font-family: 'Pretendard', sans-serif; }
.splash-fade-leave-active { transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1); }
.splash-fade-leave-to { opacity: 0; transform: scale(1.1); filter: blur(10px); }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>