<template>
  <button 
    class="btn btn-sm gap-2 transition-all duration-200"
    :class="isLiked ? 'btn-error text-white' : 'btn-outline btn-error'"
    @click.stop="$emit('toggle')"
  >
    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="isLiked ? 'fill-current' : 'fill-none'" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
    </svg>
    
    <span>{{ count }}</span>
  </button>
</template>

<script setup>
defineProps({
  isLiked: Boolean,
  count: {
    type: Number,
    default: 0
  }
})
defineEmits(['toggle'])
</script>