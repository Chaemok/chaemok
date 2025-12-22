<script setup>
const props = defineProps(['categories', 'selected'])
defineEmits(['update:selected'])
</script>

<template>
  <div class="flex gap-2 overflow-x-auto no-scrollbar py-2 px-2">
    <button 
      v-for="(config, key) in categories" :key="key"
      @click="$emit('update:selected', key)"
      class="px-6 py-3 rounded-2xl font-black text-sm transition-all border-2 whitespace-nowrap"
      :class="selected === key 
        ? 'bg-blue-900 border-blue-900 text-white shadow-lg shadow-blue-100' 
        : 'bg-white border-white text-slate-400 hover:border-blue-200 hover:text-blue-600'"
    >
      {{ config.label }}
    </button>
  </div>
</template>