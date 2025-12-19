<script setup>
defineProps(['title', 'value', 'unit', 'trend', 'trendValue', 'icon'])
</script>

<template>
  <div class="card bg-white p-6 shadow-sm border border-slate-100 hover:shadow-md transition-all cursor-pointer rounded-3xl">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2">
        <span class="p-2 bg-indigo-50 rounded-lg text-emerald-600">{{ icon }}</span>
        <h3 class="font-bold text-slate-500 text-sm">{{ title }}</h3>
      </div>
      <span v-if="trend" :class="trend === 'up' ? 'text-error' : 'text-primary'" class="text-xs font-bold">
        {{ trend === 'up' ? '▲' : '▼' }} {{ trendValue }}
      </span>
    </div>
    <div class="flex items-end gap-1">
      <span class="text-2xl font-black text-slate-800">{{ value }}</span>
      <span class="text-sm text-slate-400 mb-1">{{ unit }}</span>
    </div>
  </div>
</template>