<script setup>
defineProps({
  newsList: { type: Array, default: () => [] },
  isLoading: Boolean
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${date.getMonth()+1}.${date.getDate()} ${date.getHours()}:${date.getMinutes()}`
}
</script>

<template>
  <div class="bg-white border border-gray-200 rounded-[2rem] p-8 shadow-sm hover:shadow-xl transition-shadow duration-500 flex flex-col h-full">
    <div class="flex items-center gap-3 mb-6">
      <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-2xl">📰</div>
      <div>
        <h2 class="text-2xl font-bold">주요 경제 뉴스</h2>
        <p class="text-gray-500 text-sm">지금 가장 핫한 이슈</p>
      </div>
    </div>
    
    <div v-if="isLoading" class="flex-1 flex items-center justify-center text-gray-400">
      <span class="loading loading-spinner text-success"></span>
    </div>
    <div v-else class="flex flex-col gap-4">
      <a v-for="(news, index) in newsList" :key="index" :href="news.link" target="_blank"
         class="group p-4 hover:bg-gray-50 rounded-2xl transition-colors cursor-pointer border border-transparent hover:border-gray-100">
        <h3 class="font-bold text-gray-900 mb-1 group-hover:text-blue-600 line-clamp-1 text-lg" v-html="news.title"></h3>
        <p class="text-sm text-gray-500 line-clamp-2 mb-2 leading-relaxed" v-html="news.description"></p>
        <span class="text-xs text-gray-400">{{ formatDate(news.pubDate) }}</span>
      </a>
    </div>
  </div>
</template>