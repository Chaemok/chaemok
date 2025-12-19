<template>
  <form @submit.prevent="onSubmit" class="space-y-4">
    
    <div class="flex flex-col md:flex-row gap-4">
      <div class="form-control w-full md:w-1/2">
        <label class="label">
          <span class="label-text font-semibold">게시판</span>
        </label>
        <select 
          v-model="form.category" 
          @change="checkSecret"
          class="select select-bordered w-full focus:outline-none focus:border-primary"
        >
          <option value="free">자유게시판</option>
          <option value="qna">1:1 문의</option>
          <option value="notice" v-if="isAdmin">공지사항</option>
        </select>
      </div>

      <div class="form-control w-full md:w-1/2">
        <label class="label cursor-pointer">
          <span class="label-text font-semibold">비밀글 설정</span>
        </label>
        <label class="label cursor-pointer border rounded-lg px-4 h-[48px] hover:bg-base-200 transition">
          <span class="label-text flex items-center gap-2">
            <span v-if="form.is_secret">🔒 비밀글입니다</span>
            <span v-else>🔓 전체 공개</span>
          </span> 
          <input 
            type="checkbox" 
            class="toggle toggle-primary" 
            v-model="form.is_secret" 
          />
        </label>
      </div>
    </div>

    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">제목</span>
      </label>
      <input 
        type="text" 
        v-model="form.title" 
        placeholder="제목을 입력해 주세요" 
        class="input input-bordered w-full focus:outline-none focus:border-primary" 
        required
      />
    </div>

    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">내용</span>
      </label>
      <textarea 
        v-model="form.content" 
        class="textarea textarea-bordered h-64 focus:outline-none focus:border-primary text-base leading-relaxed" 
        placeholder="금융 정보 공유나 궁금한 점을 자유롭게 적어주세요."
        required
      ></textarea>
    </div>

    <div class="card-actions justify-end mt-6">
      <button type="button" class="btn btn-ghost" @click="$emit('cancel')">
        취소
      </button>
      <button type="submit" class="btn btn-primary px-8 text-white">
        {{ isEditMode ? '수정완료' : '등록완료' }}
      </button>
    </div>

  </form>
</template>

<script setup>
import { reactive, watch, toRefs } from 'vue'

// Props 정의: 초기 데이터(수정 시 필요)와 관리자 여부
const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      title: '',
      content: '',
      category: 'free',
      is_secret: false
    })
  },
  isAdmin: {
    type: Boolean,
    default: false
  },
  isEditMode: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

// 반응형 폼 데이터 (Props로 받은 초기값으로 시작)
const form = reactive({ ...props.initialData })

// 1:1 문의 선택 시 자동으로 비밀글 켜기 로직
const checkSecret = () => {
  if (form.category === 'qna') {
    form.is_secret = true
  }
}

// 부모에게 데이터 전송
const onSubmit = () => {
  if (!form.title.trim() || !form.content.trim()) {
    alert('제목과 내용을 모두 입력해주세요.')
    return
  }
  emit('submit', form)
}

// 수정 모드일 때 props가 늦게 로드될 경우를 대비해 watch (선택사항)
watch(() => props.initialData, (newVal) => {
  Object.assign(form, newVal)
}, { deep: true })
</script>