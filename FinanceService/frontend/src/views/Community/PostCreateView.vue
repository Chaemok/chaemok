<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()

// 폼 데이터 상태
const title = ref('')
const category = ref('free') // 기본값: 자유게시판
const content = ref('')
const isSecret = ref(false)
const isLoading = ref(false)

// 🐜 채목이의 백엔드 로직 연동: 1:1 문의 선택 시 비밀글 강제 및 비활성화
watch(category, (newVal) => {
  if (newVal === 'inquiry') {
    isSecret.value = true
  }
})

// 게시글 작성 함수
const handleSubmit = async () => {
  if (!title.value || !content.value) {
    alert('제목과 내용을 모두 입력해주세요.')
    return
  }

  isLoading.value = true
  try {
    const payload = {
      title: title.value,
      category: category.value,
      content: content.value,
      is_secret: isSecret.value
    }
    
    // DRF PostViewSet으로 POST 요청
    const res = await api.post('community/posts/', payload)
    alert('게시글이 등록되었습니다! 🐜')
    router.push({ name: 'community' }) // 목록으로 이동
  } catch (err) {
    console.error('글 작성 실패:', err)
    alert('글 등록 중 오류가 발생했습니다.')
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-12">
    <header class="mb-10 text-center">
      <h2 class="text-3xl font-black text-slate-800 tracking-tight">새 글 작성하기 ✍️</h2>
      <p class="text-slate-400 mt-2 font-medium">Smart Ants 커뮤니티에 소중한 의견을 남겨주세요.</p>
    </header>

    <div class="sa-card p-8 md:p-12 space-y-8">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="form-control w-full">
          <label class="label"><span class="label-text font-bold text-slate-500">카테고리</span></label>
          <select v-model="category" class="select select-bordered rounded-2xl border-slate-200 focus:border-primary focus:outline-none font-bold">
            <option value="free">자유게시판</option>
            <option value="qna">Q&A</option>
            <option value="review">상품후기</option>
            <option value="tips">투자꿀팁</option>
            <option value="inquiry">1:1 문의</option>
            <option value="faq">FAQ</option>
          </select>
        </div>

        <div class="form-control flex justify-end">
          <label class="label cursor-pointer justify-start gap-3 mt-8">
            <input 
              v-model="isSecret" 
              type="checkbox" 
              class="checkbox checkbox-primary rounded-lg" 
              :disabled="category === 'inquiry'"
            />
            <span class="label-text font-bold text-slate-600">비밀글로 작성하기 🔒</span>
          </label>
          <p v-if="category === 'inquiry'" class="text-[10px] text-primary font-bold ml-8">
            * 1:1 문의는 자동으로 비밀글 처리됩니다.
          </p>
        </div>
      </div>

      <div class="form-control w-full">
        <label class="label"><span class="label-text font-bold text-slate-500">제목</span></label>
        <input 
          v-model="title" 
          type="text" 
          placeholder="제목을 입력하세요" 
          class="input input-bordered w-full rounded-2xl border-slate-200 focus:border-primary focus:outline-none text-lg font-bold"
        />
      </div>

      <div class="form-control w-full">
        <label class="label"><span class="label-text font-bold text-slate-500">내용</span></label>
        <textarea 
          v-model="content" 
          class="textarea textarea-bordered h-64 rounded-2xl border-slate-200 focus:border-primary focus:outline-none text-base leading-relaxed p-6" 
          placeholder="개미들의 매너를 지켜 글을 작성해주세요. 🐜"
        ></textarea>
      </div>

      <div class="flex gap-4 pt-4">
        <button @click="router.back()" class="btn btn-ghost flex-1 rounded-2xl text-slate-400 font-bold">취소</button>
        <button 
          @click="handleSubmit" 
          class="btn btn-primary flex-[2] rounded-2xl text-white shadow-lg shadow-primary/20 font-black text-lg"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="loading loading-spinner"></span>
          등록하기
        </button>
      </div>
    </div>
  </div>
</template>