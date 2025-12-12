<!-- frontend/src/views/PostUpdateView.vue -->
<template>
  <div class="max-w-3xl mx-auto mt-10 p-4">
    <div class="card bg-base-100 shadow-xl border border-base-200">
      <div class="card-body">
        
        <h2 class="card-title text-2xl font-bold mb-6">✏️ 게시글 수정</h2>

        <PostForm 
          v-if="store.post"
          :initial-data="store.post"
          :is-edit-mode="true"
          @submit="handleUpdate"
          @cancel="router.go(-1)"
        />

        <div v-else class="flex justify-center py-20">
          <span class="loading loading-spinner loading-lg text-primary"></span>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePostStore } from '@/stores/posts'
import { useUserStore } from '@/stores/user' // user 스토어 import
import PostForm from '@/components/community/PostForm.vue' // 폴더 위치 확인 (community 폴더 안)

const store = usePostStore()
const userStore = useUserStore() // [수정] 변수명을 authStore -> userStore로 변경
const route = useRoute()
const router = useRouter()

// 페이지 로드 시 데이터 가져오기 & 권한 체크
onMounted(async () => {
  // 1. 게시글 데이터 가져오기
  await store.getPostDetail(route.params.id)

  // 2. 권한 체크 (내 글이 아니면 튕겨내기)
  // userStore.username과 게시글 작성자(user_name) 비교
  const isMyPost = userStore.username === store.post.user_name
  
  if (!isMyPost) {
    alert('수정 권한이 없습니다.')
    router.replace({ name: 'PostDetail', params: { id: route.params.id } })
  }
})

// 수정 요청 함수
const handleUpdate = async (formData) => {
  await store.updatePost(route.params.id, formData)
}
</script>