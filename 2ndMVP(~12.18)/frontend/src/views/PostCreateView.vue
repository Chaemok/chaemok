<template>
  <div class="max-w-3xl mx-auto mt-10 p-4">
    <div class="card bg-base-100 shadow-xl border border-base-200">
      <div class="card-body">
        
        <h2 class="card-title text-2xl font-bold mb-6">📝 글 작성하기</h2>

        <PostForm 
          :is-admin="isAdmin"
          @submit="handleCreate" 
          @cancel="router.go(-1)"
        />

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { usePostStore } from '@/stores/posts'
import PostForm from '@/components/community/PostForm.vue' // 컴포넌트 import

const store = usePostStore()
const router = useRouter()
const isAdmin = ref(false) // 추후 유저 정보에서 가져오기

// PostForm에서 넘어온 데이터(formData)를 받아서 저장
const handleCreate = async (formData) => {
  await store.createPost(formData)
}
</script>