<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

// 🐜 부품들 가져오기
import CommunityHeader from '@/components/community/CommunityHeader.vue'
import BoardTabs from '@/components/community/BoardTabs.vue'
import PostListItem from '@/components/community/PostListItem.vue'
import CommunityAIBriefing from '@/components/community/CommunityAIBriefing.vue'

const router = useRouter()
const posts = ref([])
const selectedCategory = ref('all')
const isLoading = ref(true)

// 🐜 카테고리 설정 (딥 블루 테마 유지)
const categoryConfig = {
  all: { label: '전체' },
  free: { label: '자유게시판', class: 'bg-blue-50 text-blue-700' },
  qna: { label: 'Q&A', class: 'bg-slate-100 text-slate-700' },
  review: { label: '상품후기', class: 'bg-emerald-50 text-emerald-700' },
  tips: { label: '투자꿀팁', class: 'bg-blue-100 text-blue-900' }, 
  inquiry: { label: '1:1 문의', class: 'bg-rose-50 text-rose-700' },
  faq: { label: 'FAQ', class: 'bg-blue-900 text-white' } 
}

const filteredPosts = computed(() => {
  if (selectedCategory.value === 'all') return posts.value
  const currentLabel = categoryConfig[selectedCategory.value]?.label
  return posts.value.filter(post => 
    post.category === selectedCategory.value || post.category === currentLabel
  )
})

const fetchPosts = async () => {
  try {
    const res = await api.get('community/posts/')
    posts.value = res.data
  } catch (err) {
    console.error('글 목록 로드 실패')
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchPosts)
</script>

<template>
  <div class="min-h-screen bg-slate-100 py-16 px-4">
    <div class="max-w-5xl mx-auto space-y-10 animate-in fade-in duration-700">
      
      <CommunityHeader />

      <CommunityAIBriefing />
      
      <BoardTabs :categories="categoryConfig" v-model:selected="selectedCategory" />

      <div v-if="!isLoading" class="space-y-5">
        <PostListItem 
          v-for="post in filteredPosts" :key="post.id" 
          :post="post" :categoryConfig="categoryConfig"
          @click="router.push({ name: 'post-detail', params: { id: post.id } })" 
          class="hover:-translate-y-1 transition-transform cursor-pointer"
        />
        
        <div v-if="filteredPosts.length === 0" 
             class="py-40 text-center bg-white/50 border-4 border-dashed border-white rounded-[3.5rem] shadow-inner">
          <div class="text-6xl mb-6 opacity-30">🐜</div>
          <p class="text-blue-900/40 font-black text-xl tracking-tighter italic">
            "이 게시판은 아직 조용하네요"
          </p>
          <p class="text-slate-400 font-bold mt-2">새로운 이야기를 먼저 시작해보세요!</p>
        </div>
      </div>
      
      <div v-else class="flex flex-col items-center justify-center py-40 space-y-4">
        <span class="loading loading-spinner loading-lg text-blue-900"></span>
        <p class="text-blue-900 font-black text-[11px] uppercase tracking-[0.3em] animate-pulse">Loading Smart Intelligence...</p>
      </div>

    </div>
  </div>
</template>