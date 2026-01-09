<script setup>
const props = defineProps(['categories', 'selected'])
defineEmits(['update:selected'])
</script>

<template>
  <div class="flex flex-wrap gap-2 py-2 px-1 justify-start">
    <button 
      v-for="(config, key) in categories" :key="key"
      @click="$emit('update:selected', key)"
      class="px-4 py-2 md:px-6 md:py-3 rounded-2xl font-black text-xs md:text-sm transition-all border-2 whitespace-nowrap text-center"
      :class="selected === key 
        ? 'bg-blue-900 border-blue-900 text-white shadow-lg shadow-blue-100' 
        : 'bg-white border-white text-slate-400 hover:border-blue-200 hover:text-blue-600'"
    >
      {{ config.label }}
    </button>
  </div>
</template>