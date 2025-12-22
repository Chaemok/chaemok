<script setup>
import { formatDate } from '@/utils/date' // 🐜 실시간 시간 포맷 사용

defineProps({
  post: Object,
  categoryConfig: Object
})
// 🐜 부모에게 클릭 이벤트를 명시적으로 보냄
defineEmits(['click'])
</script>

<template>
  <div 
    @click="$emit('click')"
    class="group bg-white/80 backdrop-blur-md px-8 py-4 flex items-center gap-6 hover:shadow-xl hover:-translate-y-0.5 transition-all cursor-pointer border border-white rounded-[2rem] shadow-sm overflow-hidden relative"
  >
    <div 
      class="absolute left-0 top-0 bottom-0 w-1.5 transition-all group-hover:w-2.5 z-0"
      :class="categoryConfig[post.category]?.class.split(' ')[1] || 'bg-blue-600'"
    ></div>

    <div class="flex items-center gap-6 w-full z-10">
      <div class="hidden sm:flex flex-col items-center justify-center w-14 h-14 rounded-2xl shadow-inner transition-transform group-hover:rotate-3 shrink-0"
           :class="categoryConfig[post.category]?.class || 'bg-slate-50'">
        <span class="text-[9px] font-black uppercase mb-0.5 tracking-tighter opacity-60">
          {{ categoryConfig[post.category]?.label || '일반' }}
        </span>
        <span class="text-xl">🐜</span>
      </div>

      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-3 mb-1">
          <span class="text-[10px] font-black text-blue-900/40 uppercase tracking-widest">
            @{{ post.user_nickname }}
          </span>
          <span class="text-[10px] font-bold text-slate-300">
            {{ formatDate(post.created_at) }}
          </span>
        </div>
        
        <h3 class="text-lg font-black text-blue-950 group-hover:text-blue-600 transition-colors flex items-center gap-2">
          <span v-if="post.is_secret" class="text-base text-blue-400">🔒</span>
          {{ post.is_secret ? '비밀글입니다.' : post.title }}
          <span v-if="post.comment_count > 0" class="text-[10px] font-black text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded-md">
            {{ post.comment_count }}
          </span>
        </h3>
      </div>

      <div class="flex items-center gap-4 border-l border-slate-50 pl-6 shrink-0">
        <div class="flex flex-col items-center text-slate-300 font-black group-hover:text-blue-600 transition-all">
          <span class="text-xl">👍</span>
          <span class="text-[10px] mt-0.5">{{ post.like_count || 0 }}</span>
        </div>
      </div>
    </div>
  </div>
</template>