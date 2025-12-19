<template>
  <div class="badge badge-primary badge-outline font-bold">
    {{ label }}
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  code: String // 'free', 'notice' 등
})

// 매핑 로직을 여기서만 관리!
const label = computed(() => {
  const map = {
    free: '자유',
    notice: '공지',
    faq: 'FAQ',
    qna: '1:1 문의'
  }
  return map[props.code] || props.code
})
</script>