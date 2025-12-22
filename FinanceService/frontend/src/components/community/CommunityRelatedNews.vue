<script setup>
defineProps({
  newsList: Array
})
</script>

<template>
  <div class="mt-8 space-y-4">
    <div class="flex items-center gap-2 px-2">
      <span class="text-[11px] font-black text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md uppercase tracking-widest">Trending News</span>
      <div class="h-[1px] flex-1 bg-slate-100"></div>
    </div>

    <div class="grid gap-3">
      <a v-for="(news, idx) in newsList" :key="idx" :href="news.url" target="_blank"
         class="group flex items-center justify-between p-4 bg-slate-50/50 border border-slate-100 rounded-2xl hover:bg-white hover:shadow-md hover:border-blue-100 transition-all">
        <div class="flex flex-col gap-1 min-w-0">
          <h4 class="text-sm font-bold text-slate-800 group-hover:text-blue-600 truncate transition-colors">
            {{ news.title }}
          </h4>
          <div class="flex items-center gap-2 text-[10px] font-bold text-slate-400">
            <span class="text-blue-900/40">{{ news.press }}</span>
            <span class="w-0.5 h-0.5 bg-slate-300 rounded-full"></span>
            <span>{{ news.time }}</span>
          </div>
        </div>
        <span class="text-slate-300 group-hover:text-blue-400 transition-colors ml-4">→</span>
      </a>
    </div>
  </div>
</template>