<script setup>
import { ref } from 'vue'
const emit = defineEmits(['submit'])
const form = ref({ username: '', nickname: '', password: '', salary: 0, risk_appetite: 3 })

const onSubmit = () => emit('submit', form.value)
</script>

<template>
  <form @submit.prevent="onSubmit" class="space-y-5">
    <div class="grid grid-cols-2 gap-4">
      <input v-model="form.username" type="text" placeholder="아이디" class="input input-bordered rounded-2xl bg-slate-50 border-slate-200 focus:border-primary font-bold" />
      <input v-model="form.nickname" type="text" placeholder="닉네임" class="input input-bordered rounded-2xl bg-slate-50 border-slate-200 focus:border-primary font-bold" />
    </div>
    <input v-model="form.password" type="password" placeholder="비밀번호" class="input input-bordered w-full rounded-2xl bg-slate-50 border-slate-200 focus:border-primary font-bold" />
    
    <div class="pt-4 border-t border-slate-100 space-y-4">
      <div class="space-y-2">
        <label class="text-xs font-black text-slate-400 ml-1">희망 연봉 (원)</label>
        <input v-model="form.salary" type="number" class="input input-bordered w-full rounded-2xl bg-slate-50 border-slate-200 focus:border-primary font-bold" />
      </div>
      <div class="space-y-2">
        <label class="text-xs font-black text-slate-400 ml-1 text-center block">투자 성향 (1:안정 ~ 5:공격)</label>
        <input v-model="form.risk_appetite" type="range" min="1" max="5" class="range range-primary range-sm" step="1" />
        <div class="w-full flex justify-between px-2 text-[10px] font-bold text-slate-400">
          <span>안정</span><span>보통</span><span>공격</span>
        </div>
      </div>
    </div>

    <button type="submit" class="btn btn-primary w-full h-14 rounded-2xl text-lg font-black mt-4 shadow-lg shadow-primary/20">
      계정 생성하기
    </button>
  </form>
</template>