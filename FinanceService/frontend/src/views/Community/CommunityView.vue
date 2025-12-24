<script setup>
import { ref, computed, onMounted, watch } from 'vue' // 🐜 watch 추가
import { useRouter, useRoute } from 'vue-router'      // 🐜 useRoute 추가
import api from '@/api'

// 부품들 가져오기
import BoardTabs from '@/components/community/BoardTabs.vue'
import PostListItem from '@/components/community/PostListItem.vue'

const router = useRouter()
const route = useRoute() // 🐜 현재 경로 정보 가져오기
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

// 🐜 [추가] URL 쿼리 파라미터를 읽어 selectedCategory에 반영하는 함수
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

// 🐜 [수정] 마운트 시 데이터 로드와 카테고리 동기화를 함께 실행
onMounted(() => {
  fetchPosts()
  syncCategoryFromQuery()
})

// 🐜 [추가] 네비바 클릭 등으로 URL의 category 쿼리가 바뀔 때 실시간 감시
watch(() => route.query.category, () => {
  syncCategoryFromQuery()
})

// 🐜 [추가] 탭을 직접 클릭했을 때 URL도 함께 바꿔주기 (뒤로가기 지원)
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
  <div class="space-y-10 animate-in fade-in duration-700">
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
        <p class="text-blue-900/40 font-black text-xl tracking-tighter italic">"이 게시판은 아직 조용하네요"</p>
        <p class="text-slate-400 font-bold mt-2">새로운 이야기를 먼저 시작해보세요!</p>
      </div>
    </div>
    
    <div v-else class="flex flex-col items-center justify-center py-40 space-y-4">
      <span class="loading loading-spinner loading-lg text-blue-900"></span>
      <p class="text-blue-900 font-black text-[11px] uppercase tracking-[0.3em] animate-pulse">Loading Community...</p>
    </div>
  </div>
</template>