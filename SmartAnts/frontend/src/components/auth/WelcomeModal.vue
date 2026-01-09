<script setup>
import Button from '@/components/ui/button/Button.vue'

defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['confirm'])
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-6 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-300">
    <div class="bg-white rounded-[32px] p-8 w-full max-w-[360px] text-center shadow-2xl animate-in slide-in-from-bottom-8 duration-500 ease-out">
      <div class="w-20 h-20 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-6">
        <span class="text-4xl animate-bounce">🎉</span>
      </div>
      
      <h2 class="text-xl font-black text-slate-900 mb-2">환영합니다!</h2>
      <p class="text-sm text-slate-500 font-medium mb-8 leading-relaxed">
        이제 스마트한 개미들의<br/>금융 커뮤니티 일원이 되었습니다.
      </p>

      <Button @click="emit('confirm')" class="w-full h-12 rounded-xl bg-slate-900 hover:bg-blue-600 text-white font-bold shadow-lg shadow-blue-100 transition-all active:scale-[0.97]">
        Smart Ants 시작하기 🐜
      </Button>
    </div>
  </div>
</template>