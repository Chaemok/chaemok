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
    <div class="relative flex items-center bg-white rounded-[2rem] shadow-lg shadow-slate-200/50 p-2 border-2 border-transparent focus-within:border-blue-500 transition-colors">
      <input 
        v-model="searchQuery"
        @keyup.enter="handleSearch"
        type="text" 
        placeholder="키워드를 입력하세요 (예: 삼성전자, 금리)"
        class="flex-1 px-6 py-3 bg-transparent text-slate-700 font-bold placeholder:text-slate-400 focus:outline-none"
      />
      <button 
        @click="handleSearch"
        class="px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-[1.5rem] font-bold text-sm transition-all shadow-md shadow-blue-200"
      >
        검색
      </button>
    </div>

    <div class="flex flex-wrap gap-2 justify-center md:justify-start">
      <button 
        v-for="cat in categories" :key="cat"
        @click="setCategory(cat)"
        :class="[
          'px-4 py-2 rounded-full text-[11px] font-bold transition-all border',
          activeCat === cat 
            ? 'bg-slate-800 border-slate-800 text-white shadow-md' 
            : 'bg-white border-slate-200 text-slate-500 hover:border-slate-400 hover:text-slate-700'
        ]"
      >
        # {{ cat }}
      </button>
    </div>
  </div>
</template>