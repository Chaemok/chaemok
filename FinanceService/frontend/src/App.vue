<script setup>
import { ref, onMounted } from 'vue'
import { RouterView, useRoute } from 'vue-router'

import TheFooter from '@/components/layout/TheFooter.vue'
import DefaultLayout from '@/components/layout/DefaultLayout.vue'
import SplashScreen from '@/components/common/SplashScreen.vue' 
import GlobalChatBot from '@/components/common/GlobalChatBot.vue'

const route = useRoute()
const isLoading = ref(true)

onMounted(async () => {
  try {
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
    
    <DefaultLayout>
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </transition>
      </RouterView>
    </DefaultLayout>

    <TheFooter />
    <GlobalChatBot />
  </div>
</template>

<style>
/* ... 기존 스타일 유지 ... */
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