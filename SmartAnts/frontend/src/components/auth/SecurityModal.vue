<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({ isOpen: Boolean })
const emit = defineEmits(['close', 'confirm'])

const password = ref('')
const passwordInput = ref(null)

// 🐜 [수정] 자동 포커스 추가
watch(() => props.isOpen, async (newVal) => {
  if (newVal) {
    await nextTick()
    passwordInput.value?.focus()
  }
})

const handleConfirm = () => {
  if (!password.value) return alert('비밀번호를 입력해주세요.')
  emit('confirm', password.value)
  password.value = ''
}
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-[999] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
    <div class="bg-white rounded-[2rem] w-full max-w-sm p-8 shadow-2xl animate-in zoom-in-95 duration-200">
      <div class="text-center mb-6">
        <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl">🔒</div>
        <h3 class="text-xl font-black text-slate-900">보안 확인</h3>
        <p class="text-sm text-slate-500 font-bold mt-2">개인정보 보호를 위해<br>비밀번호를 입력해주세요.</p>
      </div>
      <div class="space-y-4">
        <input ref="passwordInput" v-model="password" type="password" placeholder="비밀번호 입력" @keyup.enter="handleConfirm"
          class="w-full h-14 bg-slate-50 border-none rounded-2xl px-5 text-center font-bold focus:ring-2 focus:ring-blue-500 transition-all outline-none" />
        <div class="flex gap-3">
          <button @click="emit('close')" class="flex-1 h-12 rounded-xl bg-white border border-slate-200 text-slate-500 font-bold hover:bg-slate-50 transition-colors">취소</button>
          <button @click="handleConfirm" class="flex-[2] h-12 rounded-xl bg-slate-900 text-white font-bold hover:bg-blue-600 shadow-lg shadow-blue-100 transition-all active:scale-95">확인</button>
        </div>
      </div>
    </div>
  </div>
</template>