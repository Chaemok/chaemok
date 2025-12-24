<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
// 🐜 새로 만든 컴포넌트들 임포트
import YoutubeSearchBar from '@/components/youtube/YoutubeSearchBar.vue'
import YoutubeVideoCard from '@/components/youtube/YoutubeVideoCard.vue'
import YoutubePlayerModal from '@/components/youtube/YoutubePlayerModal.vue'
import BaseEmpty from '@/components/common/BaseEmpty.vue' // 👈 통합된 EmptyState

const keyword = ref('재테크')
const videos = ref([])
const isLoading = ref(false)
const selectedVideo = ref(null)
const searchBarRef = ref(null) // 자식 컴포넌트 제어용

const searchVideos = async (query) => {
  if (!query) return
  keyword.value = query // 상태 동기화
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

// 추천 검색어 클릭 시
const onTagClick = (tag) => {
  searchBarRef.value?.setKeyword(tag) // 자식 함수 호출
}

onMounted(() => { searchVideos(keyword.value) })
</script>

<template>
  <div class="min-h-screen bg-slate-50 pb-20 font-pretendard">
    <div class="max-w-7xl mx-auto px-6 pt-12">
      
      <div class="text-center mb-12 space-y-6">
        <h1 class="text-4xl font-black text-slate-900">
          <span class="text-red-600">YouTube</span> 금융 큐레이션 📺
        </h1>
        <p class="text-slate-500 text-lg">관심 있는 경제/재테크 영상을 검색해보세요.</p>
        
        <YoutubeSearchBar ref="searchBarRef" @search="searchVideos" />
        
        <div class="flex flex-wrap justify-center gap-2">
          <button v-for="tag in ['삼성전자', '환율 전망', '청년적금', '비트코인']" :key="tag"
            @click="onTagClick(tag)"
            class="px-3 py-1 bg-white border border-slate-200 rounded-full text-sm font-bold text-slate-600 hover:border-red-500 hover:text-red-500 transition-all">
            #{{ tag }}
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="flex justify-center py-20">
        <span class="loading loading-dots loading-lg text-red-600"></span>
      </div>

      <div v-else-if="videos.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <YoutubeVideoCard 
          v-for="video in videos" 
          :key="video.video_id" 
          :video="video" 
          @click="selectedVideo = video" 
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