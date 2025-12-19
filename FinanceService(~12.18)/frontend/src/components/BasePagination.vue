<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: { type: Number, required: true },
  totalPages: { type: Number, required: true }
})

const emit = defineEmits(['page-change'])

// 보여줄 페이지 번호 계산 로직 (부모에서 가져옴)
const visiblePages = computed(() => {
  const pages = []
  const total = props.totalPages
  const current = props.currentPage

  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')
    let start = Math.max(2, current - 1)
    let end = Math.min(total - 1, current + 1)
    for (let i = start; i <= end; i++) pages.push(i)
    if (current < total - 2) pages.push('...')
    if (total > 1) pages.push(total)
  }
  return pages
})

const changePage = (page) => {
  if (page >= 1 && page <= props.totalPages) {
    emit('page-change', page)
  }
}
</script>

<template>
  <div v-if="totalPages > 1" class="flex justify-center items-center gap-4 pb-10 mt-8">
    <button 
      @click="changePage(currentPage - 1)" 
      :disabled="currentPage === 1"
      class="btn btn-circle btn-sm btn-ghost hover:bg-gray-100 disabled:bg-transparent"
    >
      ❮
    </button>

    <div class="flex gap-2"> 
      <button 
        v-for="page in visiblePages" 
        :key="page"
        @click="typeof page === 'number' ? changePage(page) : null"
        class="btn btn-sm border-none min-w-[2rem] rounded-md transition-colors duration-200"
        :class="{ 
          'bg-blue-600 text-white font-bold hover:bg-blue-700': page === currentPage,
          'bg-white text-gray-600 hover:bg-gray-100': page !== currentPage && page !== '...',
          'btn-disabled bg-transparent text-gray-400 cursor-default': page === '...'
        }"
      >
        {{ page }}
      </button>
    </div>

    <button 
      @click="changePage(currentPage + 1)" 
      :disabled="currentPage === totalPages"
      class="btn btn-circle btn-sm btn-ghost hover:bg-gray-100 disabled:bg-transparent"
    >
      ❯
    </button>
  </div>
</template>