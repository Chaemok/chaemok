<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePostStore } from '@/stores/posts'

// 컴포넌트들 (CategoryTabs 삭제됨)
import PostListItem from '@/components/community/PostListItem.vue'
import SearchBar from '@/components/community/SearchBar.vue'
import Pagination from '@/components/common/Pagination.vue'

const store = usePostStore()
const router = useRouter()
const route = useRoute()

// ✨ 라우트 이름에 따른 카테고리 매핑
const getCategoryFromRoute = () => {
  switch (route.name) {
    case 'notices': return 'notice'
    case 'posts': return 'free'
    case 'faq': return 'faq'
    case 'qna': return 'qna'
    default: return 'free' // 기본값: 자유게시판
  }
}

// ✨ 현재 카테고리 이름 (화면 표시용)
const categoryTitle = computed(() => {
  const map = {
    'notice': '📢 공지사항',
    'free': '🗣️ 자유게시판',
    'faq': '❓ FAQ',
    'qna': '💬 1:1 문의'
  }
  return map[getCategoryFromRoute()] || '🗣️ 자유게시판'
})

const currentPage = ref(1)
const currentSearch = ref('')

// [수정] 데이터 가져오기 (라우트 기준)
const fetchPosts = () => {
  const category = getCategoryFromRoute()
  store.getPosts(category, currentSearch.value, currentPage.value)
}

// 검색 핸들러
const onSearch = (keyword) => {
  currentPage.value = 1
  currentSearch.value = keyword
  fetchPosts()
}

// 페이지 변경 핸들러
const onPageChange = (page) => {
  currentPage.value = page
  fetchPosts()
}

const goDetail = (id) => {
  router.push({ name: 'PostDetail', params: { id } })
}

const goCreate = () => {
  router.push({ name: 'PostCreate' })
}

// ✨ [핵심] 라우트가 바뀌면(메뉴 이동 시) 데이터 다시 로드
watch(() => route.name, () => {
  currentPage.value = 1
  currentSearch.value = ''
  fetchPosts()
})

// 초기 로딩
onMounted(() => {
  fetchPosts()
})
</script>

<template>
  <div class="max-w-4xl mx-auto mt-10 px-4 pb-20">
    
    <div class="flex flex-col mb-8">
      <h1 class="text-3xl font-bold text-base-content flex items-center gap-2">
        {{ categoryTitle }}
      </h1>
      <p class="text-gray-500 mt-2">금융 정보를 자유롭게 나누고 소통해보세요.</p>
    </div>

    <div class="flex justify-end mb-6">
      <SearchBar 
        placeholder="제목, 내용으로 검색" 
        @search="onSearch"
        class="w-full md:w-auto"
      />
    </div>

    <div class="bg-base-100 rounded-box shadow-lg border border-base-200 min-h-[300px]">
      
      <div v-if="store.loading" class="flex flex-col items-center justify-center py-20 gap-4">
        <span class="loading loading-dots loading-lg text-primary"></span>
        <span class="text-gray-400">열심히 불러오는 중...</span>
      </div>
      
      <div v-else-if="!store.posts || store.posts.length === 0" class="flex flex-col items-center justify-center py-20 text-gray-400">
        <span class="text-4xl mb-2">📭</span>
        <p>작성된 글이 없습니다.</p>
        <p class="text-sm mt-1">첫 글의 주인공이 되어보세요!</p>
      </div>

      <div v-else>
        <PostListItem 
          v-for="post in store.posts" 
          :key="post.id" 
          :post="post" 
          @click="goDetail(post.id)"
        />
      </div>
    </div>

    <Pagination 
      v-if="store.totalCount > 0"
      :current-page="currentPage"
      :total-count="store.totalCount"
      :page-size="10"
      @page-change="onPageChange"
    />

    <button 
      class="btn btn-circle btn-primary fixed bottom-10 right-10 shadow-xl w-14 h-14 z-50 text-white text-xl hover:scale-110 transition-transform"
      @click="goCreate"
      title="글쓰기"
    >
      ✏️
    </button>
  </div>
</template>