<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import CommunityHeader from '@/components/community/CommunityHeader.vue'
import PostListItem from '@/components/community/PostListItem.vue'

const router = useRouter()
const posts = ref([])
const isLoading = ref(true)

const categoryConfig = {
  inquiry: { label: '1:1 문의', class: 'bg-slate-100 text-slate-500' },
  free: { label: '자유', class: 'bg-indigo-50 text-primary' },
  review: { label: '후기', class: 'bg-amber-50 text-amber-600' },
  qna: { label: 'Q&A', class: 'bg-emerald-50 text-emerald-600' },
  tips: { label: '꿀팁', class: 'bg-purple-50 text-purple-600' },
  faq: { label: 'FAQ', class: 'bg-blue-50 text-blue-600' }
}

onMounted(async () => {
  const res = await api.get('community/posts/')
  posts.value = res.data
  isLoading.value = false
})
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-12 space-y-10">
    <CommunityHeader />
    <div class="space-y-4">
      <PostListItem v-for="post in posts" :key="post.id" 
                    :post="post" :categoryConfig="categoryConfig"
                    @click="router.push(`/community/${post.id}`)" />
    </div>
  </div>
</template>