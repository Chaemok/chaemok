<script setup>
import { ref, nextTick, defineExpose } from 'vue'
import api from '@/api'

const isChatOpen = ref(false)
const userInput = ref('')
const messages = ref([
  // 🐜 첫 인사말에 AntsBot 이름 적용
  { role: 'assistant', content: '반가워요! 저는 SmartAnts의 든든한 조력자 AntsBot입니다. 🐜 금융 상품이나 시장 상황에 대해 무엇이든 물어보세요!' }
])
const isLoading = ref(false)
const scrollRef = ref(null)

const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return

  const userMessage = userInput.value
  
  // 1. AI에게 보낼 대화 내역(History) 준비 
  // 최근 6개 정도의 메시지만 추출하여 전송 (너무 많으면 토큰 낭비)
  const history = messages.value.slice(-6).map(m => ({
    role: m.role,
    content: m.content
  }))

  // 2. 화면에 사용자 메시지 즉시 추가
  messages.value.push({ role: 'user', content: userMessage })
  userInput.value = ''
  isLoading.value = true
  
  await scrollToBottom()

  try {
    // 3. 백엔드 호출 (message와 history를 함께 전송)
    const res = await api.post('chatbot/', { 
      message: userMessage,
      history: history 
    })
    
    messages.value.push({ 
      role: 'assistant', 
      content: res.data.answer 
    })
  } catch (err) {
    console.error('AntsBot 응답 실패:', err)
    messages.value.push({ 
      role: 'assistant', 
      content: '개미굴 서버와 연결이 잠시 끊겼어요. 다시 시도해줄래? 🐜💦' 
    })
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (scrollRef.value) {
    scrollRef.value.scrollTop = scrollRef.value.scrollHeight
  }
}

const toggleChat = () => { isChatOpen.value = !isChatOpen.value }
const openChat = () => { isChatOpen.value = true }
const closeChat = () => { isChatOpen.value = false }

defineExpose({ openChat, closeChat })
</script>

<template>
  <div class="fixed bottom-8 right-8 z-[100] font-pretendard text-slate-900">
    <Transition name="slide-up">
      <div v-if="isChatOpen" 
           class="absolute bottom-20 right-0 w-[380px] h-[600px] bg-white rounded-[2rem] shadow-2xl border border-slate-100 flex flex-col overflow-hidden">
        
        <div class="p-6 bg-slate-900 text-white flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-600 rounded-2xl flex items-center justify-center text-xl shadow-lg shadow-blue-600/20">🐜</div>
            <div>
              <p class="font-black text-sm tracking-tight">AntsBot</p>
              <p class="text-[10px] text-blue-400 font-bold uppercase tracking-widest">SmartAnts AI Assistant</p>
            </div>
          </div>
          <button @click="toggleChat" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-white/10 transition-colors">✕</button>
        </div>

        <div ref="scrollRef" class="flex-1 p-6 overflow-y-auto bg-slate-50 space-y-4 scroll-smooth">
          <div v-for="(msg, idx) in messages" :key="idx" 
               :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']">
            
            <div :class="[
              'max-w-[85%] p-4 rounded-2xl text-sm leading-relaxed shadow-sm',
              msg.role === 'user' 
                ? 'bg-blue-600 text-white rounded-tr-none font-medium' 
                : 'bg-white text-slate-700 rounded-tl-none border border-slate-100'
            ]">
              {{ msg.content }}
            </div>
          </div>

          <div v-if="isLoading" class="flex justify-start">
            <div class="bg-white p-4 rounded-2xl rounded-tl-none border border-slate-100 flex items-center gap-2">
              <span class="text-xs text-slate-400 font-bold animate-pulse">AntsBot이 분석 중...</span>
              <div class="flex gap-1">
                <span class="w-1 h-1 bg-blue-400 rounded-full animate-bounce"></span>
                <span class="w-1 h-1 bg-blue-400 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                <span class="w-1 h-1 bg-blue-400 rounded-full animate-bounce [animation-delay:0.4s]"></span>
              </div>
            </div>
          </div>
        </div>

        <div class="p-4 bg-white border-t border-slate-50">
          <form @submit.prevent="sendMessage" class="flex items-center gap-2 bg-slate-100 p-2 rounded-2xl focus-within:ring-2 focus-within:ring-blue-600/20 transition-all">
            <input 
              v-model="userInput"
              type="text" 
              placeholder="개미봇에게 무엇이든 물어보세요!" 
              class="flex-1 bg-transparent border-none text-sm focus:ring-0 px-2 text-slate-700 placeholder:text-slate-400"
              :disabled="isLoading"
            />
            <button 
              type="submit"
              :disabled="isLoading || !userInput.trim()"
              class="bg-blue-600 text-white p-2.5 rounded-xl hover:bg-blue-700 disabled:bg-slate-300 transition-all"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </Transition>

    <button @click="toggleChat" 
            class="w-16 h-16 bg-slate-900 text-white rounded-full shadow-2xl flex items-center justify-center text-2xl hover:scale-110 active:scale-95 transition-all duration-300 group">
      <div class="absolute inset-0 bg-blue-600 translate-y-full group-hover:translate-y-0 transition-transform duration-300 rounded-full"></div>
      <span class="relative z-10">🐜</span>
    </button>
  </div>
</template>