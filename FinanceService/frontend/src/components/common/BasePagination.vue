<script setup>
defineProps({ currentPage: Number, totalPages: Number })
defineEmits(['page-change'])
</script>

<template>
  <div class="flex justify-center items-center gap-2 mt-12">
    <button @click="$emit('page-change', currentPage - 1)" 
            :disabled="currentPage === 1"
            class="btn btn-circle btn-ghost disabled:bg-transparent text-slate-300">〈</button>
    
    <div class="flex gap-2">
      <button v-for="page in totalPages" :key="page"
              @click="$emit('page-change', page)"
              :class="page === currentPage ? 'bg-primary text-white' : 'bg-white text-slate-400 hover:bg-slate-50'"
              class="w-10 h-10 rounded-xl font-black transition-all shadow-sm">
        {{ page }}
      </button>
    </div>

    <button @click="$emit('page-change', currentPage + 1)" 
            :disabled="currentPage === totalPages"
            class="btn btn-circle btn-ghost disabled:bg-transparent text-slate-300">〉</button>
  </div>
</template>