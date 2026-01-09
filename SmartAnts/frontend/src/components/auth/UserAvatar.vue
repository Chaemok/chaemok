<script setup>
import { computed } from 'vue'

const props = defineProps({
  image: { type: String, default: null },
  name: { type: String, default: 'Ant' },
  sizeClass: { type: String, default: 'w-10 h-10 text-sm' }
})

const bgColors = ['bg-blue-100', 'bg-indigo-100', 'bg-emerald-100', 'bg-rose-100', 'bg-amber-100']
const bgColor = computed(() => {
  const index = props.name.charCodeAt(0) % bgColors.length
  return bgColors[index]
})

const fullImageUrl = computed(() => {
  if (!props.image) return null
  if (props.image.startsWith('http')) return props.image
  
  // 🐜 [수정] 환경변수 활용
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
  return `${API_URL}${props.image}`
})
</script>

<template>
  <div class="rounded-full overflow-hidden flex items-center justify-center flex-shrink-0 border border-slate-100 shadow-sm" 
       :class="[sizeClass, !fullImageUrl ? bgColor : 'bg-white']">
    <img v-if="fullImageUrl" :src="fullImageUrl" alt="Profile" class="w-full h-full object-cover" />
    <span v-else class="font-black text-slate-600 opacity-60">{{ name.slice(0, 1) }}</span>
  </div>
</template>