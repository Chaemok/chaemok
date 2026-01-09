<script setup>
import { ref, watch } from 'vue'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'

// 🐜 부모로부터 초기 상태(내가 눌렀는지)를 받습니다.
const props = defineProps({
  postId: Number,
  likeCount: { type: Number, default: 0 },
  dislikeCount: { type: Number, default: 0 },
  isLiked: { type: Boolean, default: false },    // 추가됨
  isDisliked: { type: Boolean, default: false }  // 추가됨
})

const authStore = useAuthStore()

// 로컬 상태 (props로 초기화)
const currentLikes = ref(props.likeCount)
const currentDislikes = ref(props.dislikeCount)
const myLike = ref(props.isLiked)
const myDislike = ref(props.isDisliked)

// 🐜 Props가 변경되면(새로고침 등) 상태 업데이트
watch(() => props.likeCount, (newVal) => currentLikes.value = newVal)
watch(() => props.dislikeCount, (newVal) => currentDislikes.value = newVal)
watch(() => props.isLiked, (newVal) => myLike.value = newVal)
watch(() => props.isDisliked, (newVal) => myDislike.value = newVal)

const toggleReaction = async (type) => {
  if (!authStore.isLoggedIn) {
    alert('로그인이 필요한 기능입니다 🐜')
    return
  }

  try {
    const res = await api.post(`community/posts/${props.postId}/${type}/`)
    const { liked, disliked, like_count, dislike_count } = res.data
    
    // 서버 응답으로 모든 상태 동기화 (상호 배타적 로직은 서버가 처리)
    currentLikes.value = like_count
    currentDislikes.value = dislike_count
    
    // 🐜 내가 누른 버튼 상태 업데이트
    if (type === 'like') {
        myLike.value = liked
        // 좋아요 눌리면 싫어요는 무조건 해제
        if (liked) myDislike.value = false
    } else {
        myDislike.value = disliked
        // 싫어요 눌리면 좋아요는 무조건 해제
        if (disliked) myLike.value = false
    }

  } catch (err) {
    console.error(err)
    alert('오류가 발생했습니다.')
  }
}
</script>

<template>
  <div class="flex justify-center gap-4 py-6 bg-slate-50/50 rounded-[1.5rem] border border-slate-100">
    <button @click="toggleReaction('like')" 
      class="flex items-center gap-2 px-6 py-2.5 rounded-xl transition-all font-black text-sm border-2 active:scale-95"
      :class="myLike
        ? 'bg-blue-600 text-white border-blue-600 shadow-lg shadow-blue-100' 
        : 'bg-white text-slate-400 border-slate-200 hover:border-blue-400 hover:text-blue-600'">
      <span class="text-xl">👍</span>
      <span>좋아요 {{ currentLikes }}</span>
    </button>
    
    <button @click="toggleReaction('dislike')" 
      class="flex items-center gap-2 px-6 py-2.5 rounded-xl transition-all font-black text-sm border-2 active:scale-95"
      :class="myDislike
        ? 'bg-slate-800 text-white border-slate-800 shadow-lg' 
        : 'bg-white text-slate-400 border-slate-200 hover:border-slate-400 hover:text-slate-800'">
      <span class="text-xl">👎</span>
      <span>싫어요 {{ currentDislikes }}</span>
    </button>
  </div>
</template>