<script setup>
import { ref } from 'vue'
import { formatDate } from '@/utils/date' // 🐜 유틸리티 함수 로드
import UserAvatar from '@/components/auth/UserAvatar.vue'

const props = defineProps({
  comments: Array,
  commentCount: Number,
  isLoggedIn: Boolean
})
const emit = defineEmits(['submit-comment'])
const newComment = ref('')

const onSubmit = () => {
  if (!newComment.value.trim()) return
  emit('submit-comment', newComment.value)
  newComment.value = ''
}
</script>

<template>
  <section class="pt-12 space-y-8">
    <h3 class="text-xl font-black text-slate-800 flex items-center gap-2 px-2">
      댓글 <span class="text-slate-900 opacity-40">{{ commentCount }}</span>
    </h3>

    <div class="space-y-4">
      <div v-for="comment in comments" :key="comment.id" 
           class="p-6 bg-slate-50 rounded-[2rem] border border-slate-100/50 hover:bg-white transition-all group shadow-sm hover:shadow-md">
        <div class="flex justify-between items-center mb-4">
          <div class="flex items-center gap-3">
            <UserAvatar :name="comment.user_nickname" sizeClass="w-8 h-8 text-[10px]" />
            <span class="text-sm font-black text-slate-700">{{ comment.user_nickname }}</span>
          </div>
          <span class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">
            {{ formatDate(comment.created_at) }}
          </span>
        </div>
        <p class="text-slate-600 text-sm leading-relaxed pl-11">{{ comment.content }}</p>
      </div>
      
      <div v-if="comments?.length === 0" class="text-center py-20 text-slate-400 font-bold bg-slate-50/50 rounded-[2rem] border border-dashed border-slate-200">
        아직 작성된 댓글이 없네요. 🐜
      </div>
    </div>

    <div v-if="isLoggedIn" class="relative mt-12 animate-in fade-in slide-in-from-bottom-2">
      <textarea 
        v-model="newComment" 
        placeholder="개미들의 매너를 지켜 댓글을 남겨주세요 🐜" 
        class="textarea bg-white border-2 border-slate-100 w-full h-32 rounded-[2.5rem] focus:border-slate-900 p-6 text-base transition-all outline-none shadow-sm resize-none"
      ></textarea>
      <button @click="onSubmit" 
              class="absolute right-4 bottom-4 bg-slate-900 hover:bg-black text-white rounded-2xl px-8 h-12 font-black shadow-lg transition-transform active:scale-95 border-none">
        등록
      </button>
    </div>
    
    <div v-else class="mt-10 p-10 bg-slate-50 rounded-[2.5rem] text-center border border-dashed border-slate-200">
      <p class="text-slate-400 font-bold">로그인 후 댓글을 남길 수 있습니다 🐜</p>
    </div>
  </section>
</template>