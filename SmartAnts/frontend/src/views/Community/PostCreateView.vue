<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import PostForm from '@/components/community/PostForm.vue'

const router = useRouter()
const isLoading = ref(false)

const handleCreate = async (formData) => {
  if (!formData.title || !formData.content) {
    alert('제목과 내용을 모두 입력해주세요.')
    return
  }

  isLoading.value = true
  try {
    await api.post('community/posts/', formData)
    alert('게시글 등록 성공! 🐜')
    router.push({ name: 'community' })
  } catch (err) {
    alert('글 등록 중 오류가 발생했습니다.')
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
    
    <div class="flex items-center px-2">
      <h2 class="text-xl font-black text-slate-800 tracking-tight flex items-center gap-2">
        <span class="text-2xl">✏️</span> 새 글 작성
      </h2>
    </div>

    <PostForm 
      :loading="isLoading" 
      @submit="handleCreate" 
    />
  </div>
</template>