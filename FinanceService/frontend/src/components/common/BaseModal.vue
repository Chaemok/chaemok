<script setup>
import { watch } from 'vue'

// 🐜 모달 제어를 위한 필수 Props
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  maxWidth: {
    type: String,
    default: 'max-w-2xl'
  }
})

const emit = defineEmits(['close'])

// 🐜 [기본 디테일] 모달 오픈 시 배경 스크롤 차단
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})
</script>

<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
      
      <div 
        class="absolute inset-0 bg-slate-900/40 backdrop-blur-md transition-opacity" 
        @click="$emit('close')"
      ></div>

      <div :class="['bg-white/95 w-full rounded-[3rem] shadow-2xl overflow-hidden relative z-10 animate-fade-in-up', maxWidth]">
        
        <header class="p-10 pb-6 flex justify-between items-start">
          <div class="space-y-1">
            <slot name="header">
              <h2 v-if="title" class="text-3xl font-black text-slate-800 leading-tight">
                {{ title }}
              </h2>
            </slot>
          </div>
          <button @click="$emit('close')" class="btn btn-ghost btn-circle text-slate-300 hover:text-slate-500 text-2xl">
            ✕
          </button>
        </header>

        <main class="px-10 pb-6 overflow-y-auto max-h-[65vh] text-slate-600">
          <slot name="body"></slot>
        </main>

        <footer class="p-10 pt-4 border-t border-slate-50 flex gap-4">
          <slot name="footer"></slot>
        </footer>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* 배경 페이드 효과 */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* 모달 본체 애니메이션 */
.animate-fade-in-up {
  animation: fadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
</style>