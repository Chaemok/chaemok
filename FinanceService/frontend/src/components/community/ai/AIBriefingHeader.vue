<template>
  <div class="flex items-start justify-between">
    <div class="flex items-center gap-4">
      <div class="w-14 h-14 bg-blue-900 rounded-2xl flex items-center justify-center shadow-xl shadow-blue-100 shrink-0">
        <span class="text-2xl animate-bounce">🤖</span>
      </div>
      <div>
        <h3 class="text-xl font-black text-blue-950 tracking-tighter">{{ title }}</h3>
        <p class="text-[10px] font-black text-blue-500 uppercase tracking-[0.2em] mt-0.5">Smart Ants AI Analytics</p>
      </div>
    </div>
    <div class="px-4 py-2 bg-emerald-50 text-emerald-600 rounded-xl text-[10px] font-black border border-emerald-100 shadow-sm">
      시장 심리: {{ sentiment }} ✨
    </div>
  </div>
</template>

<script setup>
defineProps(['title', 'sentiment'])
</script>