<script setup>
defineProps({ video: Object })
defineEmits(['click'])

// HTML 엔티티 디코딩
const decodeHtml = (html) => {
  const txt = document.createElement("textarea")
  txt.innerHTML = html
  return txt.value
}
</script>

<template>
  <div 
    @click="$emit('click', video)"
    class="group bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 cursor-pointer border border-slate-100 h-full flex flex-col"
  >
    <div class="relative aspect-video overflow-hidden bg-slate-100">
      <img :src="video.thumbnail" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
      <div class="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors flex items-center justify-center">
        <span class="opacity-0 group-hover:opacity-100 text-white text-4xl drop-shadow-lg transition-opacity">▶</span>
      </div>
    </div>
    
    <div class="p-5 flex flex-col flex-1">
      <h3 class="font-bold text-slate-800 line-clamp-2 leading-snug mb-2 group-hover:text-red-600 transition-colors">
        {{ decodeHtml(video.title) }}
      </h3>
      <div class="mt-auto flex items-center justify-between text-xs font-medium text-slate-400">
        <span>{{ video.channel_title }}</span>
        <span>{{ video.publish_date }}</span>
      </div>
    </div>
  </div>
</template>