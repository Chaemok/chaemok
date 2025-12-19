<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

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
  <section class="pt-12 space-y-6">
    <h3 class="text-xl font-black text-slate-800 flex items-center gap-2">
      댓글 <span class="text-primary">{{ commentCount }}</span>
    </h3>
    <div class="space-y-4">
      <div v-for="comment in comments" :key="comment.id" class="p-6 bg-slate-50 rounded-[1.5rem] border border-slate-100">
        <div class="flex justify-between mb-2">
          <span class="text-sm font-black text-slate-700">{{ comment.user_nickname }}</span>
          <span class="text-[10px] text-slate-400 font-bold">{{ comment.created_at.split('T')[0] }}</span>
        </div>
        <p class="text-slate-600 text-sm leading-relaxed">{{ comment.content }}</p>
      </div>
    </div>
    <div v-if="isLoggedIn" class="relative mt-10">
      <textarea v-model="newComment" placeholder="댓글을 남겨주세요 🐜" 
                class="textarea textarea-bordered w-full h-32 rounded-[2rem] focus:border-primary p-6 text-base"></textarea>
      <button @click="onSubmit" class="btn btn-primary absolute right-4 bottom-4 rounded-xl px-6">등록</button>
    </div>
  </section>
</template>