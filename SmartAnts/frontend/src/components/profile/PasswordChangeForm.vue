<script setup>
import { ref } from 'vue'
const emit = defineEmits(['submit'])
const passwords = ref({ old_password: '', new_password: '', confirm_password: '' })

const onSubmit = () => {
  if (passwords.value.new_password !== passwords.value.confirm_password) {
    alert('새 비밀번호가 일치하지 않습니다.')
    return
  }
  emit('submit', passwords.value)
}
</script>

<template>
  <form @submit.prevent="onSubmit" class="space-y-6">
    <div class="space-y-2">
      <label class="text-xs font-black text-slate-400 ml-1">현재 비밀번호</label>
      <input v-model="passwords.old_password" type="password" placeholder="••••••••" class="w-full h-14 px-5 rounded-2xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-blue-500 font-bold outline-none" />
    </div>
    <div class="space-y-2">
      <label class="text-xs font-black text-slate-400 ml-1">새 비밀번호</label>
      <input v-model="passwords.new_password" type="password" placeholder="••••••••" class="w-full h-14 px-5 rounded-2xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-blue-500 font-bold outline-none" />
    </div>
    <div class="space-y-2">
      <label class="text-xs font-black text-slate-400 ml-1">새 비밀번호 확인</label>
      <input v-model="passwords.confirm_password" type="password" placeholder="••••••••" class="w-full h-14 px-5 rounded-2xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-blue-500 font-bold outline-none" />
    </div>
    
    <div class="pt-4">
      <button type="submit" class="w-full h-14 rounded-2xl bg-slate-900 text-white font-bold hover:bg-blue-600 shadow-lg shadow-blue-100 transition-all active:scale-[0.98]">
        비밀번호 변경하기 🔒
      </button>
    </div>
  </form>
</template>