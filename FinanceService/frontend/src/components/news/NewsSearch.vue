<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search'])
const searchQuery = ref('')
const categories = ['전체', '증시', '금리', '부동산', '비트코인', '절세']
const activeCat = ref('전체')

const handleSearch = () => {
  emit('search', { query: searchQuery.value, category: activeCat.value })
}

const setCategory = (cat) => {
  activeCat.value = cat
  handleSearch()
}
</script>

<template>
  <div class="space-y-6">
    <div class="relative group">
      <input 
        v-model="searchQuery"
        @keyup.enter="handleSearch"
        type="text" 
        placeholder="궁금한 경제 키워드를 입력하세요 (예: 금리, 삼성전자)"
        class="w-full px-8 py-5 bg-white border-2 border-slate-100 rounded-[2rem] text-slate-700 font-bold focus:border-blue-500 focus:outline-none shadow-lg shadow-slate-200/50 transition-all pl-14"
      />
      <span class="absolute left-6 top-1/2 -translate-y-1/2 text-xl">🔍</span>
    </div>

    <div class="flex flex-wrap gap-2 px-2">
      <button 
        v-for="cat in categories" :key="cat"
        @click="setCategory(cat)"
        :class="[
          'px-5 py-2 rounded-full text-xs font-black transition-all border-2',
          activeCat === cat 
            ? 'bg-blue-600 border-blue-600 text-white shadow-lg shadow-blue-200' 
            : 'bg-white border-slate-100 text-slate-400 hover:border-blue-200'
        ]"
      >
        # {{ cat }}
      </button>
    </div>
  </div>
</template>