<script setup>
import { ref } from 'vue'

const isChatOpen = ref(false)
const toggleChat = () => { isChatOpen.value = !isChatOpen.value }
</script>

<template>
  <div class="fixed bottom-8 right-8 z-[100] font-pretendard">
    <Transition name="slide-up">
      <div v-if="isChatOpen" 
           class="absolute bottom-20 right-0 w-[350px] h-[500px] bg-white rounded-[2.5rem] shadow-2xl border border-slate-100 flex flex-col overflow-hidden">
        
        <div class="p-6 bg-blue-600 text-white flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-white/20 rounded-xl flex items-center justify-center text-lg">🤖</div>
            <span class="font-bold tracking-tight">Smart Ants AI</span>
          </div>
          <button @click="toggleChat" class="hover:rotate-90 transition-transform">✕</button>
        </div>

        <div class="flex-1 p-6 overflow-y-auto bg-slate-50 space-y-4">
          <div class="bg-blue-100 p-4 rounded-2xl rounded-tl-none text-sm text-blue-800 self-start max-w-[80%]">
            반가워요 채목님! 🐜 어떤 금융 정보가 궁금하신가요?
          </div>
        </div>

        <div class="p-4 bg-white border-t border-slate-50">
          <div class="flex items-center gap-2 bg-slate-100 p-2 rounded-2xl">
            <input type="text" placeholder="질문을 입력하세요..." class="flex-1 bg-transparent border-none text-sm focus:ring-0 px-2" />
            <button class="bg-blue-600 text-white p-2 rounded-xl hover:bg-blue-700 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" /></svg>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <button @click="toggleChat" 
            class="w-16 h-16 bg-blue-600 text-white rounded-3xl shadow-xl shadow-blue-200 flex items-center justify-center hover:scale-110 hover:rotate-12 transition-all duration-300">
      <span v-if="!isChatOpen" class="text-3xl">🤖</span>
      <span v-else class="text-xl">✕</span>
    </button>
  </div>
</template>

<style scoped>
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translateY(30px) scale(0.9); }
</style>