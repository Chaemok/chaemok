<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const toggle = (type) => {
  emit('update:modelValue', type)
}
</script>

<template>
  <div class="flex justify-center mb-6">
    <div class="bg-gray-200 p-1.5 rounded-full inline-flex relative shadow-inner">
      <div 
        class="absolute top-1.5 bottom-1.5 w-1/2 bg-white rounded-full shadow-sm transition-all duration-300 ease-out"
        :class="modelValue === 'deposit' ? 'left-1.5' : 'left-[50%] translate-x-[-3px]'"
      ></div>

      <button 
        @click="toggle('deposit')"
        class="relative z-10 px-10 py-2 rounded-full font-bold transition-colors duration-300 text-lg w-40"
        :class="modelValue === 'deposit' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'"
      >
        예금
      </button>
      <button 
        @click="toggle('saving')"
        class="relative z-10 px-10 py-2 rounded-full font-bold transition-colors duration-300 text-lg w-40"
        :class="modelValue === 'saving' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'"
      >
        적금
      </button>
    </div>
  </div>
</template>