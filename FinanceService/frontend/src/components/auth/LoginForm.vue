<script setup>
import { ref } from 'vue'
const emit = defineEmits(['submit'])
const username = ref('')
const password = ref('')

const onSubmit = () => {
  emit('submit', { username: username.value, password: password.value })
}
</script>

<template>
  <form @submit.prevent="onSubmit" class="space-y-6">
    <div class="space-y-2">
      <label class="text-xs font-black text-slate-400 ml-1">아이디</label>
      <input v-model="username" type="text" placeholder="아이디를 입력하세요" 
        class="input input-bordered w-full h-14 rounded-2xl bg-slate-50 border-slate-200 focus:border-primary focus:bg-white transition-all font-bold text-slate-700" />
    </div>
    <div class="space-y-2">
      <label class="text-xs font-black text-slate-400 ml-1">비밀번호</label>
      <input v-model="password" type="password" placeholder="••••••••" 
        class="input input-bordered w-full h-14 rounded-2xl bg-slate-50 border-slate-200 focus:border-primary focus:bg-white transition-all font-bold text-slate-700" />
    </div>
    <button type="submit" class="btn btn-primary w-full h-14 rounded-2xl text-lg font-black shadow-lg shadow-primary/30 mt-4">
      로그인
    </button>
  </form>
</template>