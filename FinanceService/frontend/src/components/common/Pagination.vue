<template>
  <div class="join justify-center mt-8">
    <button 
      class="join-item btn" 
      :disabled="currentPage === 1"
      @click="$emit('page-change', currentPage - 1)"
    >
      «
    </button>
    
    <button 
      v-for="page in totalPages" 
      :key="page"
      class="join-item btn"
      :class="{ 'btn-active': currentPage === page }"
      @click="$emit('page-change', page)"
    >
      {{ page }}
    </button>
    
    <button 
      class="join-item btn" 
      :disabled="currentPage === totalPages"
      @click="$emit('page-change', currentPage + 1)"
    >
      »
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: { type: Number, required: true },
  totalCount: { type: Number, required: true },
  pageSize: { type: Number, default: 10 }
})

defineEmits(['page-change'])

// 총 페이지 수 계산 (예: 52개 글 / 10개씩 = 6페이지)
const totalPages = computed(() => {
  return Math.ceil(props.totalCount / props.pageSize) || 1
})
</script>