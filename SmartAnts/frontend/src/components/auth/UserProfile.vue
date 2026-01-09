<script setup>
import UserAvatar from './UserAvatar.vue'

defineProps({
  user: {
    type: Object,
    required: true
  },
  showName: { type: Boolean, default: true }
})
</script>

<template>
  <div class="flex items-center gap-3">
    <UserAvatar 
      :image="user?.profile_image" 
      :name="user?.nickname || user?.username" 
    />
    
    <div v-if="showName" class="flex flex-col">
      <span class="font-bold text-slate-800 leading-none">
        {{ user?.nickname || '부지런한 개미' }}
      </span>
      
      <span v-if="user?.username" class="text-[10px] text-slate-400 font-medium mt-1 tracking-tight">
        @{{ user.username }}
      </span>
    </div>
  </div>
</template>