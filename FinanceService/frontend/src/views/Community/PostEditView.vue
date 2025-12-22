<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import PostForm from '@/components/community/PostForm.vue'

const route = useRoute()
const router = useRouter()
const initialData = ref(null)
const loading = ref(false)

// 🐜 카테고리 이름 -> 키 변환용 매핑
const categoryMap = {
  '자유게시판': 'free', 'Q&A': 'qna', '상품후기': 'review',
  '투자꿀팁': 'tips', '1:1 문의': 'inquiry', 'FAQ': 'faq'
}

const fetchPost = async () => {
  try {
    const res = await api.get(`community/posts/${route.params.id}/`)
    const data = res.data
    
    // 🐜 [중요] 서버 데이터 로그 찍어서 확인해봐!
    console.log('불러온 데이터:', data)

    // 서버에서 온 카테고리가 한글일 경우 영문 키로 변환
    const normalizedCategory = categoryMap[data.category] || data.category

    initialData.value = {
      title: data.title,
      category: normalizedCategory,
      content: data.content,
      is_secret: data.is_secret
    }
  } catch (err) {
    console.error('데이터 로드 에러:', err)
    alert('게시글을 불러올 수 없습니다.')
    router.back()
  }
}

const handleUpdate = async (formData) => {
  loading.value = true
  try {
    await api.put(`community/posts/${route.params.id}/`, formData)
    alert('성공적으로 수정되었습니다! 🐜')
    router.push({ name: 'post-detail', params: { id: route.params.id } })
  } catch (err) {
    alert('권한이 없거나 오류가 발생했습니다.')
  } finally {
    loading.value = false
  }
}

onMounted(fetchPost)
</script>

<template>
  <div class="min-h-screen bg-slate-100 py-20 px-4">
    <div class="max-w-4xl mx-auto space-y-12">
      <header class="text-center space-y-4">
        <div class="inline-block px-4 py-1.5 bg-blue-900 text-white text-[10px] font-black rounded-full tracking-[0.3em] mb-2 shadow-lg shadow-blue-100 uppercase">
          Edit Post
        </div>
        <h2 class="text-5xl md:text-6xl font-black text-slate-900 tracking-tighter leading-tight">
          Update Your <span class="text-blue-600">Post</span>
        </h2>
      </header>

      <PostForm 
        v-if="initialData" 
        :initialData="initialData" 
        :loading="loading" 
        @submit="handleUpdate" 
      />
      
      <div v-else class="bg-white rounded-[2.5rem] p-10 md:p-14 shadow-xl shadow-slate-200/50 border border-white animate-pulse space-y-8">
        <div class="h-12 bg-slate-200 rounded-xl w-full"></div>
        <div class="h-[400px] bg-slate-100 rounded-[2.5rem] w-full"></div>
      </div>
    </div>
  </div>
</template>