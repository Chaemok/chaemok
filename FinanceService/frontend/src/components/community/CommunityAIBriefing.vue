<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const briefing = ref(null)
const isLoading = ref(true)

const fetchAIBriefing = async () => {
  isLoading.value = true
  try {
    const res = await api.get('ai/briefing/')
    briefing.value = res.data 
  } catch (err) {
    console.error('AI 브리핑 로드 실패:', err)
    briefing.value = {
      title: "브리핑을 불러올 수 없습니다",
      summary: "현재 커뮤니티 데이터를 분석하는 과정에서 오류가 발생했습니다. 🐜",
      keywords: ["연결오류"],
      sentiment: "확인불가",
      analyzed_at: "-",
      related_news: []
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchAIBriefing)
</script>

<template>
  <div v-if="isLoading" class="bg-white rounded-[3rem] p-10 animate-pulse border border-white shadow-xl shadow-slate-200/50">
    <div class="h-8 bg-slate-100 rounded-xl w-48 mb-6"></div>
    <div class="h-32 bg-slate-50 rounded-[2rem] w-full shadow-inner"></div>
  </div>

  <div v-else-if="briefing" class="bg-white rounded-[3rem] p-10 shadow-2xl shadow-slate-200/60 border border-white overflow-hidden relative group">
    <div class="absolute -top-16 -right-16 w-56 h-56 bg-blue-50/50 rounded-full blur-3xl transition-all group-hover:bg-blue-100/60"></div>

    <div class="relative space-y-8">
      <div class="flex items-start justify-between">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 bg-blue-900 rounded-2xl flex items-center justify-center shadow-xl shadow-blue-100 shrink-0">
            <span class="text-2xl animate-bounce">🤖</span>
          </div>
          <div>
            <h3 class="text-xl font-black text-blue-950 tracking-tighter">{{ briefing.title }}</h3>
            <p class="text-[10px] font-black text-blue-500 uppercase tracking-[0.2em] mt-0.5">Smart Ants AI Analytics</p>
          </div>
        </div>
        <div class="px-4 py-2 bg-emerald-50 text-emerald-600 rounded-xl text-[10px] font-black border border-emerald-100 shadow-sm">
          시장 심리: {{ briefing.sentiment }} ✨
        </div>
      </div>

      <div class="bg-slate-50 border border-slate-100 rounded-[2rem] p-8 shadow-inner relative">
        <p class="text-slate-700 leading-relaxed font-medium text-lg italic">
          "{{ briefing.summary }}"
        </p>
        <div class="mt-4 flex justify-end">
          <span class="text-[10px] font-bold text-slate-300 tracking-tight italic">
            Analyzed at {{ briefing.analyzed_at }}
          </span>
        </div>
      </div>

      <div v-if="briefing.related_news && briefing.related_news.length > 0" class="space-y-4">
        <div class="flex items-center gap-2 px-2">
          <span class="text-[10px] font-black text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md uppercase tracking-widest">Related News</span>
          <div class="h-[1px] flex-1 bg-slate-100"></div>
        </div>
        <div class="grid gap-3">
          <a v-for="(news, idx) in briefing.related_news" :key="idx" :href="news.url" target="_blank"
             class="group flex items-center justify-between p-4 bg-slate-50/50 border border-slate-100 rounded-2xl hover:bg-white hover:shadow-md transition-all">
            <div class="flex flex-col gap-1 min-w-0">
              <h4 class="text-sm font-bold text-slate-800 group-hover:text-blue-600 truncate">{{ news.title }}</h4>
              <div class="flex items-center gap-2 text-[10px] font-bold text-slate-400">
                <span class="text-blue-900/40">{{ news.press }}</span>
                <span class="w-0.5 h-0.5 bg-slate-300 rounded-full"></span>
                <span>{{ news.time }}</span>
              </div>
            </div>
            <span class="text-slate-300 group-hover:text-blue-400">→</span>
          </a>
        </div>
      </div>

      <div class="flex flex-col md:flex-row items-center justify-between gap-6 pt-2">
        <div class="flex flex-wrap gap-2">
          <span v-for="word in briefing.keywords" :key="word"
            class="px-5 py-2 bg-white border border-slate-100 rounded-full text-[11px] font-black text-blue-900/50 shadow-sm">
            # {{ word }}
          </span>
        </div>
        <button class="px-8 py-3 bg-blue-950 text-white rounded-2xl font-black text-xs shadow-xl shadow-blue-100 hover:bg-black hover:-translate-y-1 transition-all active:scale-95">
          인사이트 상세보기 🐜
        </button>
      </div>
    </div>
  </div>
</template>