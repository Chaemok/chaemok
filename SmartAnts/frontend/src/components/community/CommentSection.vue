<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { formatDate } from '@/utils/date'
import UserAvatar from '@/components/auth/UserAvatar.vue'
import api from '@/api'

const props = defineProps({
  postId: Number,
  comments: Array,
  commentCount: Number,
})

const emit = defineEmits(['refresh'])
const authStore = useAuthStore()
const newComment = ref('')
const editingId = ref(null)
const editContent = ref('')

// 🐜 상세 시간 포맷 함수
const getFullDateTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const Y = date.getFullYear()
  const M = String(date.getMonth() + 1).padStart(2, '0')
  const D = String(date.getDate()).padStart(2, '0')
  const h = String(date.getHours()).padStart(2, '0')
  const m = String(date.getMinutes()).padStart(2, '0')
  const s = String(date.getSeconds()).padStart(2, '0')
  return `${Y}.${M}.${D} ${h}:${m}:${s}`
}

// ... (기존 함수들: onSubmit, onDelete, startEdit, onUpdate, toggleReaction 생략 - 그대로 유지) ...
// 🐜 편의상 전체 코드를 드립니다.

const onSubmit = async () => {
  if (!newComment.value.trim()) return
  try {
    await api.post('community/comments/', {
      post: props.postId,
      content: newComment.value
    })
    newComment.value = ''
    emit('refresh')
  } catch (err) {
    alert('댓글 작성 실패 🐜')
  }
}

const onDelete = async (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return
  try {
    await api.delete(`community/comments/${commentId}/`)
    emit('refresh')
  } catch (err) {
    alert('삭제 실패')
  }
}

const startEdit = (comment) => {
  editingId.value = comment.id
  editContent.value = comment.content
}

const onUpdate = async (commentId) => {
  if (!editContent.value.trim()) return
  try {
    await api.put(`community/comments/${commentId}/`, {
      post: props.postId,
      content: editContent.value
    })
    editingId.value = null
    emit('refresh')
  } catch (err) {
    alert('수정 실패')
  }
}

const toggleReaction = async (id, type) => {
  if (!authStore.isLoggedIn) return alert('로그인 후 이용해주세요.')
  try {
    await api.post(`community/comments/${id}/${type}/`)
    emit('refresh')
  } catch (err) {
    console.error(err)
  }
}

const isOwner = (nickname) => authStore.user?.nickname === nickname
</script>

<template>
  <section class="pt-12 space-y-8">
    <h3 class="text-xl font-black text-slate-800 flex items-center gap-2 px-2">
      댓글 <span class="text-slate-900 opacity-40">{{ commentCount }}</span>
    </h3>

    <div class="space-y-4">
      <div v-for="comment in comments" :key="comment.id" 
           class="p-6 bg-slate-50 rounded-[2rem] border border-slate-100/50 hover:bg-white transition-all group shadow-sm hover:shadow-md relative">
        
        <div class="flex justify-between items-start mb-3">
          <div class="flex items-center gap-3">
            <UserAvatar :name="comment.user_nickname" sizeClass="w-8 h-8 text-[10px]" />
            <div class="flex flex-col">
              <span class="text-sm font-black text-slate-700 leading-none">{{ comment.user_nickname }}</span>
              <span class="text-[10px] text-slate-400 font-bold uppercase tracking-widest mt-1">
                {{ formatDate(comment.created_at) }}
              </span>
            </div>
          </div>
          
          <div class="flex flex-col items-end opacity-0 group-hover:opacity-100 transition-opacity duration-300 gap-1 absolute right-6 top-6">
            <div v-if="isOwner(comment.user_nickname) && editingId !== comment.id" class="flex gap-2">
              <button @click="startEdit(comment)" class="text-xs font-bold text-blue-500 hover:text-blue-700">수정</button>
              <button @click="onDelete(comment.id)" class="text-xs font-bold text-rose-400 hover:text-rose-600">삭제</button>
            </div>
            
            <div class="text-[9px] text-slate-300 font-medium text-right leading-tight">
              <p>{{ getFullDateTime(comment.created_at) }} 작성</p>
              <p v-if="comment.created_at !== comment.updated_at" class="text-blue-300">
                {{ getFullDateTime(comment.updated_at) }} 수정
              </p>
            </div>
          </div>
        </div>

        <div v-if="editingId === comment.id" class="pl-11 pr-2 animate-in fade-in">
          <textarea v-model="editContent" class="w-full bg-white border border-blue-200 rounded-2xl p-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-100 resize-none h-24 mb-2"></textarea>
          <div class="flex justify-end gap-2">
            <button @click="editingId = null" class="px-4 py-2 text-xs font-bold text-slate-500 bg-white border border-slate-200 rounded-xl">취소</button>
            <button @click="onUpdate(comment.id)" class="px-4 py-2 text-xs font-bold text-white bg-blue-600 rounded-xl hover:bg-blue-700">저장</button>
          </div>
        </div>
        
        <div v-else class="pl-11">
          <p class="text-slate-600 text-sm leading-relaxed whitespace-pre-wrap">{{ comment.content }}</p>
          
          <div class="flex gap-3 mt-3">
            <button @click="toggleReaction(comment.id, 'like')" 
              class="flex items-center gap-1 text-[11px] font-bold transition-colors"
              :class="comment.is_liked ? 'text-blue-600' : 'text-slate-400 hover:text-blue-600'">
              <span class="text-base">👍</span> {{ comment.like_count || 0 }}
            </button>
            <button @click="toggleReaction(comment.id, 'dislike')" 
              class="flex items-center gap-1 text-[11px] font-bold transition-colors"
              :class="comment.is_disliked ? 'text-slate-800' : 'text-slate-400 hover:text-slate-800'">
              <span class="text-base">👎</span> {{ comment.dislike_count || 0 }}
            </button>
          </div>
        </div>
      </div>
      
      <div v-if="comments?.length === 0" class="text-center py-20 text-slate-400 font-bold bg-slate-50/50 rounded-[2rem] border border-dashed border-slate-200">
        아직 작성된 댓글이 없네요. 🐜
      </div>
    </div>

    <div v-if="authStore.isLoggedIn" class="relative mt-12 animate-in fade-in slide-in-from-bottom-2">
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