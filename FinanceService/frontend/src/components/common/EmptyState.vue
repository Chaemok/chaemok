<script setup>
defineProps({
  message: { type: String, default: '조건에 맞는 상품이 없습니다.' },
  subMessage: { type: String, default: '검색 조건을 변경해보세요.' }
})
</script>

<template>
  <div class="bg-white rounded-[3rem] border border-dashed border-slate-200 py-32 text-center shadow-sm">
    <span class="text-6xl mb-6 inline-block animate-bounce">😳</span>
    <p class="text-xl font-black text-slate-700">{{ message }}</p>
    <p class="text-slate-400 font-medium">{{ subMessage }}</p>
  </div>
</template>s