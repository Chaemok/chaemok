<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  initialData: Object,
  loading: Boolean
})
const emit = defineEmits(['submit'])

const form = ref({
  title: '',
  category: 'free',
  content: '',
  is_secret: false
})

watch(() => props.initialData, (newVal) => {
  if (newVal) {
    form.value = { ...newVal }
  }
}, { immediate: true, deep: true })

const categories = {
  free: { label: '자유게시판', icon: '💬' },
  qna: { label: 'Q&A', icon: '❓' },
  review: { label: '상품후기', icon: '⭐' },
  tips: { label: '투자꿀팁', icon: '💡' },
  inquiry: { label: '1:1 문의', icon: '🔒' },
  faq: { label: 'FAQ', icon: '📢' }
}

watch(() => form.value.category, (newVal) => {
  if (newVal === 'inquiry') {
    form.value.is_secret = true
  }
})
</script>

<template>
  <div class="animate-in fade-in duration-700">
    <div class="bg-white rounded-[2.5rem] p-6 md:p-14 shadow-xl shadow-slate-200/50 border border-white space-y-8 md:space-y-10">
      
      <div class="space-y-3">
        <label class="text-[11px] font-black text-blue-900/40 uppercase tracking-[0.3em] ml-2">Category</label>
        <div class="flex flex-wrap gap-2">
          <button v-for="(val, key) in categories" :key="key"
            @click="form.category = key"
            type="button"
            class="px-4 py-2 md:px-5 md:py-2.5 rounded-2xl font-black text-xs md:text-sm transition-all border-2 whitespace-nowrap flex-grow md:flex-grow-0"
            :class="form.category === key 
              ? 'bg-blue-600 border-blue-600 text-white shadow-md shadow-blue-100' 
              : 'bg-slate-50 border-slate-50 text-slate-400 hover:border-blue-200 hover:bg-white'">
            {{ val.label }} {{ val.icon }}
          </button>
        </div>
      </div>

      <div class="space-y-3">
        <label class="text-[11px] font-black text-blue-900/40 uppercase tracking-[0.3em] ml-2">Headline</label>
        <div class="bg-slate-50 border border-slate-100 rounded-2xl shadow-inner px-6 py-4 transition-all focus-within:ring-2 focus-within:ring-blue-500/10">
          <input v-model="form.title" type="text" placeholder="제목을 입력하세요"
            class="w-full bg-transparent border-none text-lg md:text-2xl font-black text-slate-900 placeholder:text-slate-300 focus:outline-none tracking-tight" />
        </div>
      </div>

      <div class="space-y-3">
        <label class="text-[11px] font-black text-blue-900/40 uppercase tracking-[0.3em] ml-2">Content Body</label>
        <div class="relative">
          <textarea v-model="form.content" placeholder="내용을 입력하세요 🐜"
            class="w-full bg-slate-50 border border-slate-100 rounded-[2rem] px-6 py-6 md:px-8 md:py-8 h-[300px] md:h-[400px] text-base md:text-lg font-medium text-slate-700 shadow-inner focus:outline-none transition-all resize-none placeholder:text-slate-300 leading-relaxed"></textarea>
        </div>
      </div>

      <div class="flex flex-col md:flex-row items-center justify-between gap-6 pt-4">
        <label class="flex items-center gap-3 cursor-pointer group" :class="{ 'opacity-50 cursor-not-allowed': form.category === 'inquiry' }">
          <div class="relative flex items-center">
            <input type="checkbox" v-model="form.is_secret" 
              :disabled="form.category === 'inquiry'"
              class="peer h-6 w-6 cursor-pointer appearance-none rounded-full border-2 border-blue-600 transition-all checked:bg-blue-600" />
            <span class="absolute text-white opacity-0 peer-checked:opacity-100 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none text-xs">✓</span>
          </div>
          <span class="text-sm md:text-base font-bold text-slate-600 group-hover:text-blue-600 transition-colors">
            비밀글로 안전하게 보호하기 🔒
          </span>
        </label>
        
        <div class="flex gap-3 w-full md:w-auto">
          <button @click="$router.back()" type="button" class="px-6 py-4 font-black text-slate-400 hover:text-slate-800 transition-colors text-sm">
            취소
          </button>
          
          <button @click="emit('submit', form)" :disabled="loading"
            class="flex-1 md:flex-none px-10 py-4 bg-blue-950 text-white rounded-2xl font-black shadow-xl shadow-blue-200 hover:bg-blue-900 hover:-translate-y-1 transition-all active:scale-95 disabled:opacity-50 text-sm md:text-base">
            {{ loading ? '저장 중...' : '등록하기 🐜' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>