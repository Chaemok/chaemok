<template>
  <div class="min-h-screen bg-slate-50 flex flex-col pb-20">
    <header class="bg-white border-b sticky top-0 z-10 px-6 py-4 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-white text-xl">🤖</div>
        <div>
          <h1 class="font-bold text-lg text-slate-800">AI 금융 비서</h1>
          <p class="text-xs text-slate-400">당신의 상황에 맞는 최고의 상품을 찾아드립니다.</p>
        </div>
      </div>
    </header>

    <main class="flex-1 overflow-y-auto p-6 space-y-6" ref="chatContainer">
      <div class="flex items-start space-x-3">
        <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-xl">🤖</div>
        <div class="bg-white p-4 rounded-2xl rounded-tl-none shadow-sm text-slate-700 text-sm max-w-[80%]">
          안녕하세요! 👋<br>
          연봉, 자산, 원하시는 조건(예: 1년 적금, 목돈 굴리기)을 말씀해 주시면 딱 맞는 상품을 추천해 드릴게요.
        </div>
      </div>

      <div v-for="(msg, idx) in messages" :key="idx" class="flex w-full" :class="msg.isUser ? 'justify-end' : 'justify-start'">
        <div v-if="msg.isUser" class="bg-indigo-600 text-white p-3 rounded-2xl rounded-tr-none max-w-[80%] text-sm shadow-md">
          {{ msg.text }}
        </div>

        <div v-else class="flex items-start space-x-3 max-w-[90%]">
          <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-xl shrink-0">🤖</div>
          <div class="space-y-3">
            <div v-if="msg.text" class="bg-white p-4 rounded-2xl rounded-tl-none shadow-sm text-slate-700 text-sm whitespace-pre-line">
              {{ msg.text }}
            </div>

            <div v-if="msg.products && msg.products.length > 0" class="space-y-2">
              <div v-for="(prod, pIdx) in msg.products" :key="pIdx" class="bg-white p-4 rounded-xl border border-indigo-100 shadow-sm hover:shadow-md transition-shadow cursor-pointer" @click="goDetail(prod)">
                <div class="flex justify-between items-start mb-2">
                  <span class="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-1 rounded">{{ prod.bank }}</span>
                  <span class="text-xs text-slate-400">금리 정보 확인 ></span>
                </div>
                <h4 class="font-bold text-slate-800 mb-1">{{ prod.product_name }}</h4>
                <p class="text-xs text-slate-500">{{ prod.reason }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="loading" class="flex items-start space-x-3">
        <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-xl">🤖</div>
        <div class="bg-white p-4 rounded-2xl rounded-tl-none shadow-sm">
          <span class="loading loading-dots loading-sm text-indigo-400"></span>
        </div>
      </div>
    </main>

    <div class="bg-white p-4 border-t sticky bottom-0">
      <form @submit.prevent="sendMessage" class="flex space-x-2 max-w-3xl mx-auto">
        <input 
          v-model="userInput" 
          type="text" 
          placeholder="예: 연봉 4천만원인데 적금 추천해줘" 
          class="flex-1 input input-bordered bg-slate-50 focus:outline-none focus:border-indigo-500 rounded-full pl-5"
          :disabled="loading"
        />
        <button type="submit" class="btn btn-circle btn-primary text-white" :disabled="!userInput.trim() || loading">
          ➤
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const messages = ref([])
const userInput = ref('')
const loading = ref(false)
const chatContainer = ref(null)

// 스크롤 하단 이동
const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

// 메시지 전송
const sendMessage = async () => {
  if (!userInput.value.trim()) return

  // 1. 유저 메시지 표시
  const text = userInput.value
  messages.value.push({ isUser: true, text })
  userInput.value = ''
  loading.value = true
  scrollToBottom()

  try {
    // 2. 백엔드 AI API 호출 (aibot 앱)
    const res = await axios.post('http://127.0.0.1:8000/aibot/recommend/', {
      message: text // 필요 시 백엔드에서 사용자 입력도 참고하도록 수정 가능
    }, {
      headers: { Authorization: `Token ${authStore.token}` }
    })

    // 3. 응답 처리 (JSON 파싱)
    const result = res.data // { recommendations: [...] }
    
    if (result.recommendations) {
      messages.value.push({
        isUser: false,
        text: "회원님의 정보를 바탕으로 추천된 상품입니다.",
        products: result.recommendations
      })
    } else {
      messages.value.push({ isUser: false, text: "죄송해요, 적절한 상품을 찾지 못했어요." })
    }

  } catch (err) {
    console.error(err)
    messages.value.push({ isUser: false, text: "잠시 후 다시 시도해주세요. (서버 연결 실패)" })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

// 상품 상세 이동 (이름으로 검색 or ID가 있으면 ID로)
const goDetail = (prod) => {
  // 실제 구현 시엔 상품 ID가 있으면 좋지만, 없으면 이름만 보여줌
  alert(`${prod.product_name} 상세 페이지로 이동합니다. (구현 필요)`)
}
</script>