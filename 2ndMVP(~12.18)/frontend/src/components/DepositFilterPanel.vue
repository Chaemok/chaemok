<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  sector: String,      // 1금융, 2금융 선택값
  bank: String,        // 은행 선택값
  query: String,       // 검색어
  sort: String,        // 정렬 기준
  bankNames: Array     // 은행 목록 (배열)
})

const emit = defineEmits([
  'update:sector', 
  'update:bank', 
  'update:query', 
  'update:sort'
])
</script>

<template>
  <div class="bg-white rounded-3xl p-6 shadow-sm border border-gray-100 mb-8">
    
    <div class="flex justify-center mb-8">
      <div class="tabs tabs-boxed bg-gray-100 p-1 rounded-full">
        <a 
          v-for="item in [
            { label: '전체', value: 'all' },
            { label: '은행 (제1금융권)', value: '1' },
            { label: '저축은행 (제2금융권)', value: '2' }
          ]"
          :key="item.value"
          class="tab tab-lg rounded-full transition-all duration-300 px-8" 
          :class="{ 'tab-active bg-white shadow-sm text-blue-600 font-bold': sector === item.value }"
          @click="$emit('update:sector', item.value)"
        >
          {{ item.label }}
        </a>
      </div>
    </div>

    <div class="flex flex-col md:flex-row gap-4 justify-between items-center">
      
      <div class="flex flex-wrap gap-3 w-full md:w-auto">
        <select 
          :value="bank" 
          @change="$emit('update:bank', $event.target.value)"
          class="select select-bordered w-full md:w-48 rounded-xl focus:border-blue-500"
        >
          <option v-for="name in bankNames" :key="name" :value="name">
            {{ name }}
          </option>
        </select>
        
        <select 
          :value="sort"
          @change="$emit('update:sort', $event.target.value)"
          class="select select-bordered w-full md:w-36 rounded-xl"
        >
          <option value="rate">금리 순</option>
          <option value="name">가나다 순</option>
        </select>
      </div>

      <div class="relative w-full md:w-80">
        <input 
          :value="query"
          @input="$emit('update:query', $event.target.value)"
          type="text" 
          placeholder="상품명이나 은행을 검색하세요" 
          class="input input-bordered w-full rounded-xl pl-10 focus:border-blue-500"
        />
        <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tabs-boxed .tab-active {
  color: #2563eb !important;
}
</style>