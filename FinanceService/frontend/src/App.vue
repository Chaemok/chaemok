<script setup>
import { ref, onMounted } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import TheNavbar from '@/components/common/TheNavbar.vue'
import TheFooter from '@/components/layout/TheFooter.vue'
import SplashScreen from '@/components/common/SplashScreen.vue' // 아까 만든 컴포넌트

const route = useRoute()
const isLoading = ref(true)

onMounted(async () => {
  try {
    // Django API 호출 (예: 세션 확인, 유저 정보, 금융 기초 데이터)
    // await store.dispatch('initApp') 
    
    // 금융 앱의 신뢰도를 위해 최소 1.5초는 보여주는 것이 좋습니다.
    setTimeout(() => {
      isLoading.value = false
    }, 1500)
  } catch (error) {
    console.error("데이터 로딩 실패:", error)
    isLoading.value = false // 에러 시에도 진입은 시켜야 함
  }
})
</script>

<template>
  <transition name="splash-fade">
    <SplashScreen v-if="isLoading" />
  </transition>

  <div v-if="!isLoading" class="min-h-screen flex flex-col font-sans">
    <TheNavbar />

    <main class="flex-1">
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </transition>
      </RouterView>
    </main>

    <TheFooter />
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
</style>