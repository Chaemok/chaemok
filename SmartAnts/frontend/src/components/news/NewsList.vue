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
  return `${date.getFullYear()}. ${String(date.getMonth() + 1).padStart(2, '0')}. ${String(date.getDate()).padStart(2, '0')}`
}

const cleanTitle = (html) => {
  const txt = document.createElement('textarea')
  txt.innerHTML = html
  return txt.value.replace(/<[^>]*>?/gm, '')
}

// const goCommunity = (title) => {
//   router.push({ 
//     name: 'community-create', 
//     query: { title: `[뉴스토론] ${cleanTitle(title)}`, content: '이 기사에 대해 의견을 나눠봅시다.\n\n(기사 링크 첨부)' } 
//   })
// }
</script>

<template>
  <div class="w-full">
    <div v-if="isLoading" class="space-y-8 p-4">
      <div v-for="i in 5" :key="i" class="animate-pulse flex flex-col gap-4">
        <div class="h-6 bg-slate-100 rounded-xl w-3/4"></div>
        <div class="h-4 bg-slate-50 rounded-lg w-1/4"></div>
      </div>
    </div>

    <div v-else-if="!news || news.length === 0" class="text-center py-20 text-slate-400 font-medium">
      현재 불러올 수 있는 최신 뉴스가 없습니다. 😥
    </div>

    <div v-else class="divide-y divide-slate-100">
      <div v-for="(item, index) in news" :key="index" class="group px-2 py-6 hover:bg-slate-50 rounded-2xl transition-colors">
        <div class="flex flex-col gap-3">
          <div class="flex items-center gap-3">
            <span class="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded">NEWS</span>
            <span class="text-[10px] font-medium text-slate-400">{{ formatFullDate(item.pubDate) }}</span>
          </div>
          
          <a :href="item.link" target="_blank" class="block">
            <h4 class="text-lg md:text-xl font-bold text-slate-800 leading-snug group-hover:text-blue-600 transition-colors" v-html="item.title"></h4>
          </a>
          
          <p class="text-sm text-slate-500 line-clamp-2 leading-relaxed" v-html="item.description"></p>

          <div class="flex items-center gap-4 mt-2 pt-2">
            <a :href="item.link" target="_blank" class="text-xs font-bold text-slate-400 hover:text-slate-800 hover:underline">
              전문 보기
            </a>
            <span class="text-slate-200 text-xs">|</span>
            <!-- <button 
              @click="goCommunity(item.title)"
              class="text-xs font-bold text-slate-500 hover:text-transparent hover:bg-clip-text hover:bg-gradient-to-r hover:from-blue-600 hover:to-indigo-600 transition-all flex items-center gap-1"
            >
              이 이슈로 토론하기
              <span class="text-slate-400">💬</span>
            </button> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>