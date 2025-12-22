<script setup>
import { ref } from 'vue'
import Button from '@/components/ui/button/Button.vue'

const props = defineProps({ isOpen: Boolean })
const emit = defineEmits(['close', 'confirm'])

const password = ref('')

const handleConfirm = () => {
  emit('confirm', password.value)
  password.value = '' // 입력값 초기화
}
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-slate-900/60 backdrop-blur-md">
    <div class="bg-white rounded-[32px] p-8 w-full max-w-[400px] shadow-2xl animate-in zoom-in-95 duration-300">
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4">
          <span class="text-3xl">🔒</span>
        </div>
        <h2 class="text-xl font-black text-slate-900">보안 확인</h2>
        <p class="text-sm text-slate-500 font-medium mt-2">정보 보호를 위해 비밀번호를 입력해주세요.</p>
      </div>

      <input 
        v-model="password"
        type="password" 
        placeholder="현재 비밀번호 입력"
        class="w-full h-14 bg-slate-50 border-none rounded-2xl px-5 text-center font-bold focus:ring-2 focus:ring-primary transition-all mb-4"
        @keyup.enter="handleConfirm"
      />

      <div class="flex gap-3">
        <Button @click="emit('close')" class="flex-1 h-12 rounded-xl bg-slate-100 text-slate-500 hover:bg-slate-200 font-bold">취소</Button>
        <Button @click="handleConfirm" class="flex-1 h-12 rounded-xl bg-slate-900 text-white font-bold">확인</Button>
      </div>
    </div>
  </div>
</template>