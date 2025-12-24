<script setup>
defineProps({
  title: { type: String, default: '데이터가 없습니다.' },
  description: { type: String, default: '' },
  icon: { type: String, default: '📭' } // 이모지나 아이콘 클래스
})
</script>

<template>
  <div class="flex flex-col items-center justify-center py-20 text-center animate-in fade-in zoom-in-95 duration-300">
    <div class="text-6xl mb-4 opacity-80">{{ icon }}</div>
    <h3 class="text-xl font-black text-slate-800 mb-2">{{ title }}</h3>
    <p v-if="description" class="text-slate-500 max-w-sm mx-auto leading-relaxed">
      {{ description }}
    </p>
    <div v-if="$slots.default" class="mt-6">
      <slot />
    </div>
  </div>
</template>