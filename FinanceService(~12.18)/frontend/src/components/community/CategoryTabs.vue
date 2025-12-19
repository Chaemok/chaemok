<template>
  <div class="tabs tabs-boxed bg-base-100 p-0 mb-6 gap-2">
    <a 
      v-for="tab in tabs" 
      :key="tab.value"
      class="tab transition-all duration-200"
      :class="{ 'tab-active bg-primary text-white font-bold rounded-lg': currentTab === tab.value }"
      @click="$emit('change', tab.value)"
    >
      {{ tab.label }}
    </a>
  </div>
</template>

<script setup>
defineProps({
  currentTab: String,
  tabs: Array
})

defineEmits(['change'])
</script>