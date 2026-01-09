<script setup>
import { ref, onMounted, computed } from 'vue' 
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'
import CommentSection from '@/components/community/CommentSection.vue' 
import PostReaction from '@/components/community/PostReaction.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const post = ref(null)

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
  <div v-if="post" class="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
    
    <div class="flex justify-between items-center px-2">
      <button @click="router.push({ name: 'community' })" 
        class="flex items-center gap-2 px-4 py-2 bg-white/50 backdrop-blur-sm rounded-xl font-bold text-xs text-slate-600 hover:bg-white hover:text-blue-600 hover:shadow-sm transition-all border border-transparent hover:border-white">
        <span>←</span> 목록으로
      </button>

      <div v-if="isOwnerOrAdmin" class="flex gap-2">
        <button @click="router.push({ name: 'post-edit', params: { id: post.id } })" 
                class="px-4 py-2 bg-indigo-50/80 backdrop-blur-sm text-indigo-600 rounded-xl font-bold text-xs hover:bg-indigo-100 transition-colors">
          수정
        </button>
        <button @click="deletePost" 
                class="px-4 py-2 bg-rose-50/80 backdrop-blur-sm text-rose-600 rounded-xl font-bold text-xs hover:bg-rose-100 transition-colors">
          삭제
        </button>
      </div>
    </div>

    <div class="bg-white rounded-[2.5rem] shadow-xl shadow-slate-200/50 border border-white p-8 md:p-12 space-y-8">
      <header class="space-y-6 border-b border-slate-50 pb-6">
        <div class="flex items-center justify-between">
          <span class="px-4 py-1.5 bg-blue-600 text-white text-[10px] font-black rounded-full tracking-widest uppercase shadow-md shadow-blue-100">
            {{ post.category || 'COMMUNITY' }}
          </span>
        </div>

        <div class="space-y-4">
          <h1 class="text-3xl md:text-4xl font-black text-slate-900 leading-tight tracking-tighter">
            {{ post.title }}
          </h1>
          
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-slate-50 rounded-full flex items-center justify-center font-black text-blue-600 shadow-inner border border-slate-100">
              {{ post.user_nickname?.charAt(0) }}
            </div>
            <div class="flex flex-col">
              <p class="text-sm font-black text-slate-800">@{{ post.user_nickname }}</p>
              <div class="flex items-center gap-2 text-[11px] font-bold text-slate-400">
                <span>{{ getFullDateTime(post.created_at) }}</span>
                <span v-if="post.created_at !== post.updated_at" class="text-blue-400">
                  (수정됨: {{ getFullDateTime(post.updated_at) }})
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div class="text-slate-700 text-lg leading-relaxed whitespace-pre-wrap font-medium min-h-[120px]">
        {{ post.content }}
      </div>

      <div class="flex justify-center pt-8">
        <div class="w-full max-w-sm">
          <PostReaction 
            :postId="post.id" 
            :likeCount="post.like_count || 0" 
            :dislikeCount="post.dislike_count || 0"
            :isLiked="post.is_liked"
            :isDisliked="post.is_disliked"
          />
        </div>
      </div>
    </div>

    <div class="bg-white rounded-[2.5rem] p-8 md:p-10 shadow-lg shadow-slate-200/40 border border-white">
      <CommentSection 
        :postId="post.id"
        :comments="post.comments" 
        :commentCount="post.comment_count" 
        @refresh="fetchPost"
      />
    </div>
  </div>
</template>