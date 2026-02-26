<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'

const store = useUserStore()

// 부모에게서 받을 정보 (이미지 경로, 이름, 크기 클래스)
const props = defineProps({
  image: { type: String, default: null },
  name: { type: String, default: 'ME' },
  sizeClass: { type: String, default: 'w-12 h-12 text-lg' } // 기본 크기
})

// URL 계산 로직 (여기에만 존재하면 됨)
const fullImageUrl = computed(() => {
  if (!props.image) return null
  if (props.image.startsWith('http')) return props.image
  return `${store.API_URL}${props.image}`
})
</script>

<template>
  <div class="rounded-full overflow-hidden border border-gray-100 bg-gray-50 flex items-center justify-center flex-shrink-0" :class="sizeClass">
    <img v-if="fullImageUrl" :src="fullImageUrl" class="w-full h-full object-cover" />
    
    <span v-else class="font-bold text-gray-400 select-none">
      {{ name.substring(0, 2).toUpperCase() }}
    </span>
  </div>
</template>