<template>
  <div 
    class="flex items-center justify-between p-4 border-b border-base-200 hover:bg-base-100 cursor-pointer transition-colors"
    @click="$emit('click')"
  >
    <div class="flex flex-col gap-1 w-full">
      <div class="flex items-center gap-2">
        <CategoryBadge :code="post.category" />
        
        <h3 class="text-lg font-medium truncate">
          {{ post.title }}
        </h3>
        
        <span v-if="post.is_secret" class="text-lg" title="비밀글">🔒</span>
      </div>

      <div class="text-xs text-gray-400 flex items-center gap-2 mt-1">
        <span class="font-semibold text-gray-500">{{ post.user_name }}</span>
        <span>·</span>
        <span class="flex items-center gap-1">
          ❤️ {{ post.like_count }}
        </span>
        <span>·</span>
        <span>{{ new Date(post.created_at).toLocaleDateString() }}</span>
      </div>
    </div>

    <div class="text-gray-300">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
    </div>
  </div>
</template>

<script setup>
import CategoryBadge from '@/components/common/CategoryBadge.vue'

defineProps({
  post: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])
</script>