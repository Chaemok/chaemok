<script setup>
import { ref } from 'vue'

// 🐜 [수정] 로딩 상태 props 추가
defineProps({ isLoading: Boolean })
const emit = defineEmits(['submit'])

const username = ref('')
const password = ref('')

const onSubmit = () => {
  emit('submit', { username: username.value, password: password.value })
}
</script>

<template>
  <form @submit.prevent="onSubmit" class="space-y-6">
    <div class="space-y-2 animate-stagger-1">
      <label class="text-[11px] font-black text-slate-400 uppercase tracking-widest ml-1">아이디</label>
      <input v-model="username" type="text" placeholder="아이디를 입력하세요" 
        class="w-full h-12 px-4 rounded-xl border border-slate-100 bg-slate-50/50 focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all font-bold text-slate-900 outline-none" />
    </div>

    <div class="space-y-2 animate-stagger-2">
      <label class="text-[11px] font-black text-slate-400 uppercase tracking-widest ml-1">비밀번호</label>
      <input v-model="password" type="password" placeholder="••••••••" 
        class="w-full h-12 px-4 rounded-xl border border-slate-100 bg-slate-50/50 focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all font-bold text-slate-900 outline-none" />
    </div>

    <div class="pt-2 animate-stagger-3">
      <button type="submit" :disabled="isLoading"
        class="w-full h-12 rounded-xl bg-slate-900 hover:bg-blue-600 text-white font-bold text-sm shadow-xl shadow-slate-200 transition-all active:scale-[0.97] disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2">
        <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
        {{ isLoading ? '로그인 중...' : '로그인' }}
      </button>
    </div>
  </form>
</template>

<style scoped>
[class^="animate-stagger-"] { opacity: 0; animation: slideUpStagger 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; }
@keyframes slideUpStagger { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-stagger-1 { animation-delay: 0.1s; }
.animate-stagger-2 { animation-delay: 0.2s; }
.animate-stagger-3 { animation-delay: 0.3s; }
</style>