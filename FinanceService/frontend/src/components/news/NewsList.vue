<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  news: Array,
  isLoading: Boolean
})

const router = useRouter()

const formatFullDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
}

const goCommunity = (title) => {
  router.push({ 
    name: 'community-create', 
    query: { title: `[뉴스토론] ${title}`, content: '이 뉴스에 대해 어떻게 생각하시나요?' } 
  })
}
</script>

<template>
  <div class="w-full">
    <div v-if="isLoading" class="space-y-8 p-4">
      <div v-for="i in 5" :key="i" class="animate-pulse flex flex-col gap-4">
        <div class="h-6 bg-slate-100 rounded-xl w-3/4"></div>
        <div class="h-4 bg-slate-50 rounded-lg w-1/4"></div>
      </div>
    </div>

    <div v-else class="divide-y divide-slate-50">
      <div v-for="(item, index) in news" :key="index" class="group relative px-4 py-8 hover:bg-slate-50/50 transition-all rounded-[2rem]">
        <div class="flex flex-col gap-4">
          <div class="flex items-center gap-3">
            <span class="text-[10px] font-black text-blue-600 bg-blue-50 px-2 py-0.5 rounded uppercase tracking-wider">Market News</span>
            <span class="text-[10px] font-bold text-slate-400">{{ formatFullDate(item.pubDate) }}</span>
          </div>
          
          <a :href="item.link" target="_blank" class="block">
            <h4 class="text-xl font-black text-slate-800 leading-snug group-hover:text-blue-600 transition-colors line-clamp-2">
              {{ item.title }}
            </h4>
          </a>

          <div class="flex items-center justify-between">
            <a :href="item.link" target="_blank" class="text-xs font-bold text-slate-400 hover:text-slate-600 underline">기사 원문보기</a>
            <button 
              @click="goCommunity(item.title)"
              class="px-4 py-2 bg-white border border-slate-200 rounded-xl text-[11px] font-black text-slate-600 hover:bg-blue-600 hover:text-white hover:border-blue-600 transition-all shadow-sm"
            >
              커뮤니티에서 토론하기 💬
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>