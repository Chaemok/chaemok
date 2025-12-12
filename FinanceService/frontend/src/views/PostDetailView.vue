<!-- frontend/src/views/PostDetailView.vue -->
<template>
  <div class="max-w-4xl mx-auto mt-10 px-4 mb-20">
    
    <div v-if="!post" class="flex justify-center py-20">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>

    <div v-else class="card bg-base-100 shadow-xl border border-base-200">
      <div class="card-body">
        
        <div class="flex items-center gap-2 mb-2">
          <CategoryBadge :code="post.category" />
          <span class="text-sm text-gray-500">
            {{ new Date(post.created_at).toLocaleString() }}
          </span>
        </div>

        <h1 class="card-title text-3xl font-bold mb-4 text-gray-800">
          {{ post.title }}
        </h1>

        <div class="divider my-0"></div>

        <div class="flex justify-between items-center py-2">
          <UserProfile :name="post.user_name" />

          <LikeButton 
            :is-liked="post.is_liked" 
            :count="post.like_count" 
            @toggle="onLike" 
          />
        </div>

        <div class="py-8 text-lg leading-loose whitespace-pre-wrap text-gray-700 min-h-[200px]">
          {{ post.content }}
        </div>

        <div class="card-actions justify-end mt-4 items-center">
          
          <div class="flex gap-2 mr-auto" v-if="isMyPost">
            <button class="btn btn-outline btn-primary btn-sm" @click="goEdit">
              수정
            </button>
            <button class="btn btn-outline btn-error btn-sm" @click="onDelete">
              삭제
            </button>
          </div>

          <button class="btn btn-ghost" @click="router.push({ name: 'community' })">
            목록으로 돌아가기
          </button>
        </div>

      </div>
    </div>

    <CommentSection 
      v-if="post" 
      :comments="post.comments" 
      :postId="post.id"
      @refresh="fetchData" 
    />

  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePostStore } from '@/stores/posts'
import { useUserStore } from '@/stores/user' // [중요] user 스토어 사용

// 분리한 컴포넌트들 import (경로 확인 필수!)
// 만약 components 폴더 정리를 아직 안 하셨다면 경로를 맞춰주세요.
import CommentSection from '@/components/community/CommentSection.vue'
import CategoryBadge from '@/components/common/CategoryBadge.vue'
import LikeButton from '@/components/common/LikeButton.vue'
import UserProfile from '@/components/common/UserProfile.vue'

const store = usePostStore()
const userStore = useUserStore() // 유저 정보 가져오기
const route = useRoute()
const router = useRouter()

const post = computed(() => store.post)

// [권한 체크 로직]
// 1. 로그인 상태여야 함 (isLogin)
// 2. 게시글 데이터가 있어야 함 (store.post)
// 3. 내 아이디(username)와 작성자(user_name)가 같아야 함
const isMyPost = computed(() => {
  return userStore.isLogin && 
         store.post && 
         userStore.username === store.post.user_name
})

const fetchData = () => {
  store.getPostDetail(route.params.id)
}

onMounted(() => {
  fetchData()
})

const onLike = () => {
  store.likePost(route.params.id)
}

// 수정 페이지로 이동
const goEdit = () => {
  router.push({ name: 'PostUpdate', params: { id: route.params.id } })
}

// 삭제 요청
const onDelete = () => {
  store.deletePost(route.params.id)
}
</script>