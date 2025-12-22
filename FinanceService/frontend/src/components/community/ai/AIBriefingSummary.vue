<template>
  <div class="bg-slate-50 border border-slate-100 rounded-[2rem] p-8 shadow-inner relative">
    <p class="text-slate-700 leading-relaxed font-medium text-lg italic">
      "{{ summary }}"
    </p>
    <div class="mt-4 flex justify-end">
      <span class="text-[10px] font-bold text-slate-300 tracking-tight italic">
        Analyzed at {{ analyzedAt }}
      </span>
    </div>
  </div>
</template>

<script setup>
defineProps(['summary', 'analyzedAt'])
</script>