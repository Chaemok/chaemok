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
  <div class="min-h-screen bg-slate-100 py-20 px-4">
    <div class="max-w-4xl mx-auto space-y-12">
      
      <header class="text-center space-y-4 animate-in fade-in slide-in-from-top-4 duration-700">
        <div class="inline-block px-4 py-1.5 bg-blue-900 text-white text-[10px] font-black rounded-full tracking-[0.3em] mb-2 shadow-lg shadow-blue-100 uppercase">
          New Post
        </div>
        <h2 class="text-5xl md:text-6xl font-black text-slate-900 tracking-tighter leading-tight">
          Share Your <span class="text-blue-600">Wisdom.</span>
        </h2>
        <p class="text-slate-400 font-bold uppercase tracking-widest text-[13px] opacity-80">
          개미들과 나누고 싶은 금융 지식을 자유롭게 적어보세요 🐜
        </p>
      </header>

      <PostForm 
        :loading="isLoading" 
        @submit="handleCreate" 
      />
    </div>
  </div>
</template>