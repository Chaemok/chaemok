<script setup>
defineProps({
  post: Object,
  categoryConfig: Object
})
</script>

<template>
  <div class="sa-card p-6 flex items-center gap-6 hover:shadow-md transition-all cursor-pointer group border border-slate-50">
    <div class="hidden sm:flex flex-col items-center justify-center w-16 h-16 rounded-2xl transition-colors"
         :class="categoryConfig[post.category]?.class || 'bg-slate-50'">
      <span class="text-[10px] font-black uppercase mb-1">{{ categoryConfig[post.category]?.label }}</span>
      <span class="text-xl">🐜</span>
    </div>
    <div class="flex-1">
      <p class="text-xs text-slate-400 font-medium mb-1">{{ post.user_nickname }} · {{ post.created_at.split('T')[0] }}</p>
      <h3 class="text-lg font-bold text-slate-700 group-hover:text-primary transition-colors flex items-center gap-2">
        <span v-if="post.is_secret" class="text-sm opacity-50">🔒</span>
        {{ post.is_secret ? '비밀글입니다.' : post.title }}
        <span v-if="post.comment_count > 0" class="text-xs text-primary font-medium">[{{ post.comment_count }}]</span>
      </h3>
    </div>
    <div class="flex items-center gap-4 text-slate-300 font-bold text-xs">
      <div class="flex items-center gap-1"><span>👍</span> {{ post.like_count }}</div>
    </div>
  </div>
</template>