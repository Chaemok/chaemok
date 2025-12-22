<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const props = defineProps({
  image: { type: String, default: null },
  name: { type: String, default: 'Ant' },
  sizeClass: { type: String, default: 'w-10 h-10 text-sm' }
})

// 🐜 [Aesthetic] 이름에 따라 배경색을 다르게 주면 훨씬 예뻐!
const bgColors = ['bg-blue-100', 'bg-indigo-100', 'bg-emerald-100', 'bg-rose-100', 'bg-amber-100']
const bgColor = computed(() => {
  const index = props.name.charCodeAt(0) % bgColors.length
  return bgColors[index]
})

const fullImageUrl = computed(() => {
  if (!props.image) return null
  if (props.image.startsWith('http')) return props.image
  // 🐜 백엔드 주소(http://127.0.0.1:8000)와 경로 결합
  return `http://127.0.0.1:8000${props.image}`
})
</script>

<template>
  <div class="rounded-full overflow-hidden flex items-center justify-center flex-shrink-0 border border-slate-100 shadow-sm" 
       :class="[sizeClass, !fullImageUrl ? bgColor : 'bg-white']">
    
    <img v-if="fullImageUrl" :src="fullImageUrl" class="w-full h-full object-cover" />
    
    <span v-else class="font-black text-slate-600 select-none tracking-tighter">
      {{ name.substring(0, 2).toUpperCase() }}
    </span>
  </div>
</template>