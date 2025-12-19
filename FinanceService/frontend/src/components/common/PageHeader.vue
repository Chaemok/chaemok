<script setup>
defineProps({
  title: String,
  subtitle: String,
  emoji: { type: String, default: '💰' }
})
</script>

<template>
  <header class="space-y-2">
    <h2 class="text-3xl font-black text-slate-800 flex items-center gap-3">
      <span class="text-4xl">{{ emoji }}</span> {{ title }}
    </h2>
    <p class="text-slate-400 font-bold">{{ subtitle }}</p>
  </header>
</template>