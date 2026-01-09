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
    class="group bg-white rounded-[2rem] overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 cursor-pointer border border-slate-100 h-full flex flex-col"
  >
    <div class="relative aspect-video overflow-hidden bg-slate-100">
      <img :src="video.thumbnail" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
      <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center">
        <div class="w-12 h-12 bg-red-600 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transform scale-50 group-hover:scale-100 transition-all duration-300 shadow-lg">
          <span class="text-white text-xl ml-1">▶</span>
        </div>
      </div>
    </div>
    
    <div class="p-6 flex flex-col flex-1">
      <h3 class="font-bold text-slate-800 line-clamp-2 leading-snug mb-3 group-hover:text-red-600 transition-colors">
        {{ decodeHtml(video.title) }}
      </h3>
      <div class="mt-auto flex items-center justify-between text-xs font-bold text-slate-400 border-t border-slate-50 pt-4">
        <span class="flex items-center gap-1">
          📺 {{ video.channel_title }}
        </span>
        <span>{{ video.publish_date }}</span>
      </div>
    </div>
  </div>
</template>