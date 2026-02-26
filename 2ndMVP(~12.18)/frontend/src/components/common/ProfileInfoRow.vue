<script setup>
defineProps({
  label: String,
  value: [String, Number] // 문자나 숫자 모두 받을 수 있게
})
</script>

<template>
  <div>
    <label class="text-xs text-gray-400 font-bold block mb-1">{{ label }}</label>
    <div class="font-medium text-gray-900 break-words">
      <slot>{{ value || '-' }}</slot>
    </div>
  </div>
</template>