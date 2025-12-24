<script setup>
import { ref } from 'vue'

const keyword = ref('')
const emit = defineEmits(['search'])

const onSearch = () => {
  if (keyword.value.trim()) emit('search', keyword.value)
}

// 부모가 키워드를 바꿀 수 있게 (추천 검색어 클릭 시 등)
const setKeyword = (val) => {
  keyword.value = val
  onSearch()
}

defineExpose({ setKeyword })
</script>

<template>
  <div class="relative max-w-xl mx-auto w-full">
    <input 
      v-model="keyword" 
      @keyup.enter="onSearch"
      type="text" 
      placeholder="검색어를 입력하세요 (예: 청년도약계좌)" 
      class="w-full pl-6 pr-14 py-4 rounded-full border-2 border-slate-200 text-lg font-bold focus:outline-none focus:border-red-500 focus:ring-4 focus:ring-red-500/10 transition-all shadow-lg shadow-slate-200/50"
    />
    <button 
      @click="onSearch"
      class="absolute right-3 top-1/2 -translate-y-1/2 p-2 bg-red-600 text-white rounded-full hover:bg-red-700 transition-colors w-10 h-10 flex items-center justify-center"
    >
      🔍
    </button>
  </div>
</template>