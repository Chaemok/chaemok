<script setup>
defineProps({
  text: String,
  color: { type: String, default: 'gray' }, // gray, blue, red 등
  size: { type: String, default: 'md' }     // sm, md, lg
})
</script>

<template>
  <button 
    class="btn border-none font-bold rounded-xl transition-all duration-200"
    :class="{
      'bg-gray-800 text-white hover:bg-gray-700': color === 'gray',
      'bg-blue-600 text-white hover:bg-blue-700': color === 'blue',
      'bg-red-500 text-white hover:bg-red-600': color === 'red',
      'bg-white text-gray-900 hover:bg-gray-100': color === 'white',
      'btn-sm text-xs': size === 'sm',
      'btn-md text-base': size === 'md',
      'btn-lg text-lg': size === 'lg'
    }"
  >
    <slot>{{ text }}</slot>
  </button>
</template>