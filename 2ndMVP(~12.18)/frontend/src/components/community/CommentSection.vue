<template>
  <div class="mt-10">
    <h3 class="text-xl font-bold mb-4 flex items-center gap-2">
      💬 댓글 <span class="text-primary">{{ comments.length }}</span>
    </h3>

    <div v-if="userStore.isLogin" class="flex gap-2 mb-8">
      <input 
        v-model="content" 
        type="text" 
        placeholder="따뜻한 댓글을 남겨주세요..." 
        class="input input-bordered w-full focus:outline-none focus:border-primary" 
        @keyup.enter="onSubmit"
      />
      <button 
        class="btn btn-primary text-white" 
        @click="onSubmit"
        :disabled="!content.trim()"
      >
        등록
      </button>
    </div>
    <div v-else class="alert alert-warning shadow-sm mb-6 text-sm py-2">
      <span>댓글을 작성하려면 로그인이 필요합니다.</span>
    </div>

    <div class="space-y-4">
      <div 
        v-for="comment in comments" 
        :key="comment.id" 
        class="bg-base-100 p-4 rounded-xl border border-base-200 shadow-sm transition-hover hover:shadow-md"
      >
        <div class="flex justify-between items-start mb-2">
          <div class="flex items-center gap-2">
            <div class="avatar placeholder">
              <div class="bg-neutral text-neutral-content rounded-full w-8 h-8">
                <span class="text-xs">{{ comment.user_name?.substring(0, 2) }}</span>
              </div>
            </div>
            <div>
              <span class="font-bold text-sm block">{{ comment.user_name }}</span>
              <span class="text-xs text-gray-400">{{ new Date(comment.created_at).toLocaleString() }}</span>
            </div>
          </div>

          <button 
            v-if="userStore.username === comment.user_name"
            class="btn btn-ghost btn-xs text-gray-400 hover:text-error"
            @click="onDelete(comment.id)"
          >
            삭제 🗑️
          </button>
        </div>

        <p class="text-gray-700 text-sm pl-10">{{ comment.content }}</p>
      </div>

      <div v-if="comments.length === 0" class="text-center py-10 text-gray-400 bg-base-100 rounded-xl border border-dashed border-base-300">
        아직 작성된 댓글이 없습니다.<br />첫 번째 댓글을 남겨보세요! 👋
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const props = defineProps({
  comments: Array,
  postId: Number
})

const emit = defineEmits(['refresh']) // 댓글 작성/삭제 후 부모에게 "데이터 다시 불러와!" 신호 보냄
const userStore = useUserStore()
const content = ref('')

// 댓글 작성
const onSubmit = async () => {
  if (!content.value.trim()) return

  try {
    await axios.post(`http://127.0.0.1:8000/api/posts/${props.postId}/comments/`, 
      { content: content.value },
      { headers: { Authorization: `Bearer ${userStore.token}` }}
    )
    content.value = '' // 입력창 비우기
    emit('refresh')    // 목록 갱신 요청
  } catch (err) {
    console.error(err)
    alert('댓글 작성 실패!')
  }
}

// 댓글 삭제
const onDelete = async (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return

  try {
    await axios.delete(`http://127.0.0.1:8000/api/comments/${commentId}/`, {
      headers: { Authorization: `Bearer ${userStore.token}` }
    })
    emit('refresh') // 목록 갱신 요청
  } catch (err) {
    console.error(err)
    alert('삭제 실패!')
  }
}
</script>