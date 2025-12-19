<template>
  <div class="flex items-center gap-2">
    <div class="avatar placeholder">
      <div class="bg-neutral-focus text-neutral-content rounded-full w-8 bg-gray-600 text-white">
        <span class="text-xs">{{ name.substring(0, 2) }}</span>
      </div>
    </div>
    <span class="font-semibold text-gray-700">{{ name }}</span>
  </div>
</template>

<script setup>
defineProps({
  name: {
    type: String,
    default: 'User'
  }
})
</script>