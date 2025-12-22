<script setup>
import { ref, onMounted, computed } from 'vue' 
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'
import { formatDate } from '@/utils/date' 
import CommentSection from '@/components/community/CommentSection.vue' 
import PostReaction from '@/components/community/PostReaction.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const post = ref(null)

// 🐜 날짜/시간 전체 표기 함수 (2025.12.22 15:22:22)
const getFullDateTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const Y = date.getFullYear()
  const M = String(date.getMonth() + 1).padStart(2, '0')
  const D = String(date.getDate()).padStart(2, '0')
  const h = String(date.getHours()).padStart(2, '0')
  const m = String(date.getMinutes()).padStart(2, '0')
  const s = String(date.getSeconds()).padStart(2, '0')
  return `(${Y}.${M}.${D} ${h}:${m}:${s})`
}

const isOwnerOrAdmin = computed(() => {
  if (!post.value || !authStore.user) return false
  return authStore.user.nickname === post.value.user_nickname || authStore.user.is_staff 
})

const deletePost = async () => {
  if (!confirm('정말 삭제할까요? 🐜')) return
  try {
    await api.delete(`community/posts/${route.params.id}/`)
    router.push({ name: 'community' }) 
  } catch (err) { alert('권한이 없습니다.') }
}

const fetchPost = async () => {
  try {
    const res = await api.get(`community/posts/${route.params.id}/`)
    post.value = res.data
  } catch (err) { 
    console.error(err)
    router.push({ name: 'community' }) 
  }
}

onMounted(async () => {
  if (authStore.token && !authStore.user) await authStore.getUserInfo()
  fetchPost()
})
</script>

<template>
  <div class="min-h-screen bg-slate-100 py-12 px-4">
    <div v-if="post" class="max-w-3xl mx-auto space-y-6 animate-in fade-in duration-700">
      
      <div class="flex justify-between items-center px-2">
        <button @click="router.back()" 
          class="flex items-center gap-2 px-5 py-2.5 bg-white rounded-2xl font-black text-[11px] text-slate-500 shadow-sm border border-white hover:text-blue-600 transition-all">
          <span>←</span> 목록
        </button>

        <div v-if="isOwnerOrAdmin" class="flex gap-2 bg-white/80 backdrop-blur-md p-1.5 rounded-2xl shadow-sm border border-white">
          <button @click="router.push({ name: 'post-edit', params: { id: post.id } })" 
                  class="px-5 py-2.5 bg-indigo-50 text-indigo-500 rounded-xl font-black text-[11px] hover:bg-indigo-100 transition-colors">
            수정 ✏️
          </button>
          <button @click="deletePost" 
                  class="px-5 py-2.5 bg-rose-50 text-rose-500 rounded-xl font-black text-[11px] hover:bg-rose-100 transition-colors">
            삭제 🗑️
          </button>
        </div>
      </div>

      <div class="bg-white rounded-[2.5rem] shadow-xl shadow-slate-200/50 border border-white p-8 md:p-10 space-y-8">
        <header class="space-y-6">
          <div class="flex items-center justify-between">
            <span class="px-4 py-1.5 bg-blue-600 text-white text-[10px] font-black rounded-full tracking-widest uppercase shadow-md shadow-blue-100">
              {{ post.category || 'COMMUNITY' }}
            </span>
            <span v-if="post.updated_at && post.created_at !== post.updated_at" 
                  class="text-[10px] font-bold text-slate-400 bg-slate-50 px-3 py-1 rounded-lg border border-slate-100">
              최종 수정: {{ getFullDateTime(post.updated_at) }}
            </span>
          </div>

          <h1 class="text-3xl md:text-4xl font-black text-slate-900 leading-tight tracking-tighter">
            {{ post.title }}
          </h1>
          
          <div class="flex items-center gap-4 p-4 bg-slate-50/50 rounded-[1.5rem] w-full border border-slate-100">
            <div class="w-12 h-12 bg-white rounded-2xl flex items-center justify-center font-black text-blue-600 text-xl shadow-sm shrink-0 border border-blue-50">
              {{ post.user_nickname?.charAt(0) }}
            </div>
            <div class="flex flex-col">
              <p class="text-base font-black text-slate-800">@{{ post.user_nickname }}</p>
              <div class="flex flex-wrap items-center gap-1.5 text-[10px] font-bold text-slate-400">
                <span class="text-blue-500/60">{{ formatDate(post.created_at) }} 작성</span>
                <span class="font-medium opacity-60">{{ getFullDateTime(post.created_at) }}</span>
              </div>
            </div>
          </div>
        </header>

        <div class="text-slate-600 text-[17px] leading-relaxed whitespace-pre-wrap font-medium min-h-[120px] px-2">
          {{ post.content }}
        </div>

        <div class="pt-6 border-t border-slate-50 flex justify-center">
          <div class="w-full max-w-sm">
            <PostReaction 
              :postId="post.id" 
              :likeCount="post.like_count || 0" 
              :dislikeCount="post.dislike_count || 0" 
            />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-[2.5rem] p-8 md:p-10 shadow-lg shadow-slate-200/40 border border-white">
        <CommentSection 
          :comments="post.comments" 
          :commentCount="post.comment_count" 
          :isLoggedIn="authStore.isLoggedIn" 
        />
      </div>
    </div>
  </div>
</template>