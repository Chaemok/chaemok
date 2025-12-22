<script setup>
import { ref } from 'vue'
import api from '@/api'

const props = defineProps({
  postId: Number,
  likeCount: { type: Number, default: 0 },    // 🐜 기본값 0으로 에러 방지
  dislikeCount: { type: Number, default: 0 } // 🐜 NaN 방지 핵심!
})

const localLike = ref(false)
const localDislike = ref(false)

const toggleReaction = async (type) => {
  try {
    // 🐜 실제 API 연동 시: await api.post(`community/posts/${props.postId}/${type}/`)
    if (type === 'like') {
      localLike.value = !localLike.value
      if (localLike.value) localDislike.value = false
    } else {
      localDislike.value = !localDislike.value
      if (localDislike.value) localLike.value = false
    }
  } catch (err) {
    alert('반응을 반영하지 못했습니다 🐜')
  }
}
</script>

<template>
  <div class="flex justify-center gap-4 py-6 bg-slate-50/50 rounded-[1.5rem] border border-slate-100">
    
    <button @click="toggleReaction('like')" 
      class="flex items-center gap-2 px-6 py-2.5 rounded-xl transition-all font-black text-sm border-2"
      :class="localLike 
        ? 'bg-blue-600 text-white border-blue-600 shadow-lg shadow-blue-100' 
        : 'bg-white text-slate-400 border-slate-200 hover:border-blue-400 hover:text-blue-600'">
      <span class="text-xl">👍</span>
      <span>좋아요 {{ (likeCount || 0) + (localLike ? 1 : 0) }}</span>
    </button>
    
    <button @click="toggleReaction('dislike')" 
      class="flex items-center gap-2 px-6 py-2.5 rounded-xl transition-all font-black text-sm border-2"
      :class="localDislike 
        ? 'bg-slate-800 text-white border-slate-800 shadow-lg' 
        : 'bg-white text-slate-400 border-slate-200 hover:border-slate-400 hover:text-slate-800'">
      <span class="text-xl">👎</span>
      <span>싫어요 {{ (dislikeCount || 0) + (localDislike ? 1 : 0) }}</span>
    </button>
  </div>
</template>