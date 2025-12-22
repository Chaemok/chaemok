<script setup>
defineProps({
  keywords: Array
})
</script>

<template>
  <div class="flex flex-col md:flex-row items-center justify-between gap-6 pt-2">
    <div class="flex flex-wrap gap-2">
      <span v-for="word in keywords" :key="word"
            class="px-5 py-2 bg-white border border-slate-100 rounded-full text-[11px] font-black text-blue-900/50 shadow-sm">
        # {{ word }}
      </span>
    </div>
    <button class="px-8 py-3 bg-blue-950 text-white rounded-2xl font-black text-xs shadow-xl shadow-blue-100 hover:bg-black hover:-translate-y-1 transition-all active:scale-95">
      인사이트 상세보기 🐜
    </button>
  </div>
</template>