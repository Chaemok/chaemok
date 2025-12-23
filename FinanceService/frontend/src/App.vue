<script setup>
import { ref, onMounted } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import TheNavbar from '@/components/common/TheNavbar.vue'
import TheFooter from '@/components/layout/TheFooter.vue'
import SplashScreen from '@/components/common/SplashScreen.vue' 
// 🤖 챗봇 컴포넌트 임포트 확인
import GlobalChatBot from '@/components/common/GlobalChatBot.vue'

const route = useRoute()
const isLoading = ref(true)

onMounted(async () => {
  try {
    // 🐜 금융 앱의 신뢰도를 위해 최소 1.5초 노출
    setTimeout(() => {
      isLoading.value = false
    }, 1500)
  } catch (error) {
    console.error("데이터 로딩 실패:", error)
    isLoading.value = false
  }
})
</script>

<template>
  <transition name="splash-fade">
    <SplashScreen v-if="isLoading" />
  </transition>

  <div v-if="!isLoading" class="min-h-screen flex flex-col font-sans relative">
    
    <TheNavbar />

    <main class="flex-1">
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </transition>
      </RouterView>
    </main>

    <TheFooter />

    <GlobalChatBot />
  </div>
</template>

<style>
/* 기존 페이드 효과 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 스플래시 전용 부드러운 사라짐 효과 */
.splash-fade-leave-active {
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}
.splash-fade-leave-to {
  opacity: 0;
  transform: scale(1.05); /* 살짝 커지면서 사라지는 고급 효과 */
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.splash-fade-leave-active {
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}
.splash-fade-leave-to {
  opacity: 0;
  transform: scale(1.05);
}
</style>