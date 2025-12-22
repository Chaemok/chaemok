<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  initialData: Object, // Edit 시 전달됨
  loading: Boolean     // 버튼 로딩 상태
})
const emit = defineEmits(['submit'])

// 🐜 내부 폼 상태 (초기값 설정)
const form = ref({
  title: '',
  category: 'free',
  content: '',
  is_secret: false
})

// 🐜 [핵심] props.initialData 감시: 데이터가 들어올 때만 폼에 복사 (Edit 용)
watch(() => props.initialData, (newVal) => {
  if (newVal) {
    form.value = { ...newVal }
  }
}, { immediate: true, deep: true })

// 🐜 카테고리 설정
const categories = {
  free: { label: '자유게시판', icon: '💬' },
  qna: { label: 'Q&A', icon: '❓' },
  review: { label: '상품후기', icon: '⭐' },
  tips: { label: '투자꿀팁', icon: '💡' },
  inquiry: { label: '1:1 문의', icon: '🔒' },
  faq: { label: 'FAQ', icon: '📢' }
}

// 🐜 1:1 문의 비밀글 강제 적용 로직
watch(() => form.value.category, (newVal) => {
  if (newVal === 'inquiry') {
    form.value.is_secret = true
  }
})
</script>

<template>
  <div class="space-y-10 animate-in fade-in duration-700">
    <div class="flex gap-2 overflow-x-auto no-scrollbar px-2 py-1">
      <button v-for="(val, key) in categories" :key="key"
        @click="form.category = key"
        type="button"
        class="px-6 py-3 rounded-2xl font-black text-sm transition-all border-2 whitespace-nowrap"
        :class="form.category === key 
          ? 'bg-blue-600 border-blue-600 text-white shadow-lg shadow-blue-100' 
          : 'bg-white border-slate-100 text-slate-400 hover:border-blue-200'">
        {{ val.label }} {{ val.icon }}
      </button>
    </div>

    <div class="bg-white rounded-[2.5rem] p-10 md:p-14 shadow-xl shadow-slate-200/50 border border-white space-y-10">
      
      <div class="space-y-3">
        <label class="text-[11px] font-black text-blue-900/40 uppercase tracking-[0.3em] ml-2">Headline</label>
        <div class="bg-slate-50 border border-slate-100 rounded-2xl shadow-inner px-8 py-5 transition-all focus-within:ring-2 focus-within:ring-blue-500/10">
          <input v-model="form.title" type="text" placeholder="제목을 입력하세요"
            class="w-full bg-transparent border-none text-2xl font-black text-slate-900 placeholder:text-slate-200 focus:outline-none tracking-tighter" />
        </div>
      </div>

      <div class="space-y-3">
        <label class="text-[11px] font-black text-blue-900/40 uppercase tracking-[0.3em] ml-2">Content Body</label>
        <div class="relative">
          <textarea v-model="form.content" placeholder="내용을 입력하세요 🐜"
            class="w-full bg-slate-50 border border-slate-100 rounded-[2.5rem] px-10 py-12 h-[400px] text-lg font-medium text-slate-700 shadow-inner focus:outline-none transition-all resize-none placeholder:text-slate-300 leading-relaxed"></textarea>
        </div>
      </div>

      <div class="flex flex-col md:flex-row items-center justify-between gap-6 pt-4">
        <label class="flex items-center gap-3 cursor-pointer group" :class="{ 'opacity-50 cursor-not-allowed': form.category === 'inquiry' }">
          <div class="relative flex items-center">
            <input type="checkbox" v-model="form.is_secret" 
              :disabled="form.category === 'inquiry'"
              class="peer h-7 w-7 cursor-pointer appearance-none rounded-full border-2 border-blue-600 transition-all checked:bg-blue-600" />
            <span class="absolute text-white opacity-0 peer-checked:opacity-100 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none text-xs">✓</span>
          </div>
          <span class="text-base font-bold text-slate-600 group-hover:text-blue-600 transition-colors">
            비밀글로 안전하게 보호하기 🔒
          </span>
        </label>
        
        <div class="flex gap-4 w-full md:w-auto">
          <button @click="$router.back()" type="button" class="px-8 py-4 font-black text-slate-400 hover:text-slate-800 transition-colors uppercase tracking-widest text-xs">Cancel</button>
          
          <button @click="emit('submit', form)" :disabled="loading"
            class="flex-1 md:flex-none px-12 py-4 bg-blue-950 text-white rounded-2xl font-black shadow-xl shadow-blue-200 hover:bg-blue-900 hover:-translate-y-1 transition-all active:scale-95 disabled:opacity-50">
            {{ loading ? 'SAVING...' : 'PUBLISH 🐜' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>