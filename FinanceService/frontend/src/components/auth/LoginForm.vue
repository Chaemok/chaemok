<script setup>
import { ref } from 'vue'
import Input from '@/components/ui/input/Input.vue'
import Label from '@/components/ui/label/Label.vue'
import Button from '@/components/ui/button/Button.vue'

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
      <Label for="username" class="text-[11px] font-black text-slate-400 uppercase tracking-widest ml-1">아이디</Label>
      <Input id="username" v-model="username" type="text" placeholder="아이디를 입력하세요" 
        class="h-12 px-4 rounded-xl border-slate-100 bg-slate-50/50 focus-visible:ring-blue-500 focus-visible:bg-white transition-all font-medium text-slate-900 shadow-sm" />
    </div>

    <div class="space-y-2 animate-stagger-2">
      <div class="flex justify-between items-center ml-1">
        <Label for="password" class="text-[11px] font-black text-slate-400 uppercase tracking-widest">비밀번호</Label>
        <!-- <a href="#" class="text-[10px] font-bold text-blue-500 hover:text-blue-600 transition-colors">비밀번호 찾기</a> -->
      </div>
      <Input id="password" v-model="password" type="password" placeholder="••••••••" 
        class="h-12 px-4 rounded-xl border-slate-100 bg-slate-50/50 focus-visible:ring-blue-600 focus-visible:bg-white transition-all font-medium text-slate-900 shadow-sm" />
    </div>

    <div class="pt-2 animate-stagger-3">
      <Button type="submit" 
        class="w-full h-12 rounded-xl bg-slate-900 hover:bg-blue-600 text-white font-bold text-sm shadow-xl shadow-slate-200 transition-all active:scale-[0.97]">
        로그인
      </Button>
    </div>

  </form>
</template>

<style scoped>
/* 🐜 순차적 슬라이드 애니메이션 정의 */
[class^="animate-stagger-"] {
  opacity: 0;
  animation: slideUpStagger 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-stagger-1 { animation-delay: 0.1s; }
.animate-stagger-2 { animation-delay: 0.2s; }
.animate-stagger-3 { animation-delay: 0.3s; }
.animate-stagger-4 { animation-delay: 0.4s; }

@keyframes slideUpStagger {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

:deep(.focus-visible\:ring-blue-500) {
  --tw-ring-color: rgb(37 99 235);
}
</style>