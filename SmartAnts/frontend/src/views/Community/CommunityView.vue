<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/api'
import BoardTabs from '@/components/community/BoardTabs.vue'
import PostListItem from '@/components/community/PostListItem.vue'

const router = useRouter()
const route = useRoute()
const posts = ref([])
const selectedCategory = ref('all')
const isLoading = ref(true)

const categoryConfig = {
  all: { label: '전체' },
  free: { label: '자유게시판', class: 'bg-blue-50 text-blue-700' },
  qna: { label: 'Q&A', class: 'bg-slate-100 text-slate-700' },
  review: { label: '상품후기', class: 'bg-emerald-50 text-emerald-700' },
  tips: { label: '투자꿀팁', class: 'bg-blue-100 text-blue-900' },   
  faq: { label: 'FAQ', class: 'bg-blue-900 text-white' },
  inquiry: { label: '1:1 문의', class: 'bg-rose-50 text-rose-700' },
}

const syncCategoryFromQuery = () => {
  const queryCat = route.query.category
  if (queryCat && categoryConfig[queryCat]) {
    selectedCategory.value = queryCat
  } else {
    selectedCategory.value = 'all'
  }
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

onMounted(() => {
  fetchPosts()
  syncCategoryFromQuery()
})

watch(() => route.query.category, syncCategoryFromQuery)
watch(selectedCategory, (newCat) => {
  if (route.query.category !== newCat) {
    router.push({ 
      name: 'community', 
      query: newCat === 'all' ? {} : { category: newCat } 
    })
  }
})
</script>

<template>
  <div class="space-y-6 animate-in fade-in duration-700">
    
    <div class="w-full bg-white rounded-[2rem] p-4 shadow-xl shadow-slate-200/50 flex flex-wrap md:flex-nowrap items-center justify-between gap-4 border border-slate-100">
      
      <div class="w-full md:w-auto">
        <BoardTabs :categories="categoryConfig" v-model:selected="selectedCategory" />
      </div>
      
      <button @click="router.push({ name: 'post-create' })" 
        class="hidden md:flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-2xl font-black shadow-lg shadow-blue-100 hover:bg-blue-700 hover:-translate-y-1 transition-all active:scale-95 shrink-0 whitespace-nowrap ml-auto">
        <span>✏️</span> 새로운 글 작성
      </button>
    </div>

    <div class="md:hidden flex justify-center">
      <button @click="router.push({ name: 'post-create' })" 
        class="flex items-center gap-2 px-8 py-3 bg-blue-600 text-white rounded-[2rem] font-black shadow-lg active:scale-95 transition-transform text-sm">
        <span>✏️</span> 새로운 글 작성하기
      </button>
    </div>

    <div v-if="!isLoading" class="space-y-4">
      <PostListItem 
        v-for="post in filteredPosts" :key="post.id" 
        :post="post" :categoryConfig="categoryConfig"
        @click="router.push({ name: 'post-detail', params: { id: post.id } })" 
        class="hover:-translate-y-1 transition-transform cursor-pointer"
      />
      
      <div v-if="filteredPosts.length === 0" 
           class="py-32 text-center bg-white/50 border-4 border-dashed border-white rounded-[3.5rem] shadow-inner">
        <div class="text-6xl mb-6 opacity-30 grayscale">🐜</div>
        <p class="text-blue-900/40 font-black text-xl tracking-tighter italic">"이 게시판은 아직 조용하네요"</p>
        <p class="text-slate-400 font-bold mt-2 text-sm">새로운 이야기를 먼저 시작해보세요!</p>
      </div>
    </div>
    
    <div v-else class="flex flex-col items-center justify-center py-40 space-y-4">
      <span class="loading loading-spinner loading-lg text-blue-900"></span>
      <p class="text-blue-900 font-black text-[11px] uppercase tracking-[0.3em] animate-pulse">Loading Community...</p>
    </div>
  </div>
</template>