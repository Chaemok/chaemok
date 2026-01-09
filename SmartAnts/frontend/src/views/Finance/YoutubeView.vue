<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import YoutubeSearchBar from '@/components/youtube/YoutubeSearchBar.vue'
import YoutubeVideoCard from '@/components/youtube/YoutubeVideoCard.vue'
import YoutubePlayerModal from '@/components/youtube/YoutubePlayerModal.vue'
import BaseEmpty from '@/components/common/BaseEmpty.vue'
import PageHeader from '@/components/common/PageHeader.vue'

const keyword = ref('')
const videos = ref([])
const isLoading = ref(false)
const selectedVideo = ref(null)
const searchBarRef = ref(null)

// 🐜 비트코인 제외하고 실용적인 금융 키워드로 구성
const randomKeywords = [
  '사회초년생 재테크', '2025 경제 전망', '주식 초보 가이드', 
  '부동산 시장 전망', 'ISA 계좌 장점', '청년 도약 계좌', 
  '연말정산 꿀팁', 'ETF 추천', '노후 연금 준비', '짠테크 방법',
  '미국 주식 하는법', '금리 인하 영향'
]

const searchVideos = async (query) => {
  if (!query) return
  keyword.value = query 
  isLoading.value = true
  
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/finlife/youtube/', {
      params: { keyword: query }
    })
    videos.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

const onTagClick = (tag) => {
  searchBarRef.value?.setKeyword(tag) 
}

onMounted(() => {
  // 랜덤 키워드로 초기 검색
  const randomKey = randomKeywords[Math.floor(Math.random() * randomKeywords.length)]
  keyword.value = randomKey
  searchVideos(randomKey)
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 font-pretendard">
    
    <PageHeader 
      title="YouTube Financial Curation" 
      subtitle="경제/재테크 영상을 검색하여  금융 지식을 넓혀보세요."
      bgClass="bg-red-700" 
    />

    <div class="max-w-7xl mx-auto px-4 pb-20 -mt-8 relative z-20">
      
      <div class="bg-white rounded-[2.5rem] p-8 shadow-xl shadow-slate-200/50 border border-white mb-10 text-center space-y-6">
        <h2 class="text-2xl font-black text-slate-800">
          오늘은 <span class="text-red-600">"{{ keyword }}"</span> 관련 영상 어때요? 📺
        </h2>
        
        <YoutubeSearchBar ref="searchBarRef" @search="searchVideos" />
        
        <div class="flex flex-wrap justify-center gap-2">
          <button v-for="tag in ['삼성전자', '환율 전망', '청년적금', 'ISA 계좌', '미국주식', '부동산']" :key="tag"
            @click="onTagClick(tag)"
            class="px-4 py-2 bg-slate-50 border border-slate-200 rounded-full text-sm font-bold text-slate-600 hover:border-red-500 hover:text-red-500 hover:bg-white transition-all active:scale-95">
            #{{ tag }}
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="flex justify-center py-40">
        <span class="loading loading-dots loading-lg text-red-600"></span>
      </div>

      <div v-else-if="videos.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <YoutubeVideoCard 
          v-for="video in videos" 
          :key="video.video_id" 
          :video="video" 
          @click="selectedVideo = video" 
          class="hover:-translate-y-2 transition-transform duration-300"
        />
      </div>

      <BaseEmpty v-else title="검색 결과가 없습니다." description="다른 키워드로 검색해보거나, 철자를 확인해주세요." icon="🤔" />

    </div>

    <YoutubePlayerModal 
      :isOpen="!!selectedVideo" 
      :videoId="selectedVideo?.video_id" 
      @close="selectedVideo = null" 
    />
  </div>
</template>

<style scoped>
.font-pretendard { font-family: 'Pretendard', sans-serif; }
</style>