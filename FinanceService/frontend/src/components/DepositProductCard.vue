<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['click-card'])
</script>

<template>
  <div 
    class="group bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 cursor-pointer relative overflow-hidden"
    @click="emit('click-card', product.id)"
  >
    <div class="absolute top-0 right-0 w-24 h-24 bg-blue-50 rounded-bl-full -mr-4 -mt-4 opacity-0 group-hover:opacity-100 transition-opacity"></div>

    <div class="flex items-start justify-between mb-4 relative z-10">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-gray-50 flex items-center justify-center text-lg shadow-inner">
          🏦
        </div>
        <div>
          <span class="text-xs font-bold text-blue-600 block mb-0.5">{{ product.bank_name }}</span>
          <h3 class="font-bold text-gray-800 text-lg leading-tight group-hover:text-blue-600 transition-colors line-clamp-1">
            {{ product.product_name }}
          </h3>
        </div>
      </div>
    </div>

    <div class="space-y-3 relative z-10">
      <div class="flex justify-between items-center py-2 border-b border-gray-50">
        <span class="text-gray-400 text-sm">기본 금리</span>
        <span class="font-medium text-gray-600">{{ product.interest_rate }}%</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-400 text-sm">최고 우대 금리</span>
        <span class="text-2xl font-extrabold text-emerald-500">{{ product.highest_rate }}%</span>
      </div>
    </div>

    <div class="mt-4 flex gap-2">
      <span v-if="product.join_term" class="px-2 py-1 bg-gray-100 text-gray-500 text-xs rounded-md">
         📅 {{ product.join_term }}
      </span>
    </div>
  </div>
</template>