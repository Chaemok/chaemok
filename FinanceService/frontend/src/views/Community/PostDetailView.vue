<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'
import CommentSection from '@/components/community/CommentSection.vue'

const route = useRoute()
const authStore = useAuthStore()
const post = ref(null)

const fetchPost = async () => {
  const res = await api.get(`community/posts/${route.params.id}/`)
  post.value = res.data
}

const handleCommentSubmit = async (content) => {
  await api.post(`community/posts/${post.value.id}/comments/`, { content })
  fetchPost()
}

onMounted(fetchPost)
</script>

<template>
  <div v-if="post" class="max-w-3xl mx-auto px-4 py-12 space-y-8">
    <article class="space-y-6">
      <h2 class="text-3xl font-black text-slate-800 leading-tight">{{ post.title }}</h2>
      <div class="sa-card p-10 min-h-[300px] text-slate-700 leading-relaxed whitespace-pre-wrap">
        {{ post.content }}
      </div>
    </article>

    <CommentSection :comments="post.comments" 
                    :commentCount="post.comment_count" 
                    :isLoggedIn="authStore.isLoggedIn"
                    @submit-comment="handleCommentSubmit" />
  </div>
</template>