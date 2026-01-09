<script setup>
const props = defineProps({
  type: String,   // 🐜 추가: 예금/적금 상태
  sector: String,
  bank: String,
  query: String,
  sort: String,
  bankNames: Array
})

const emit = defineEmits(['update:type', 'update:sector', 'update:bank', 'update:query', 'update:sort'])
</script>

<template>
  <div class="space-y-8">
    
    <div class="flex justify-center">
      <div class="bg-slate-100 p-1.5 rounded-2xl inline-flex gap-1">
        <button @click="emit('update:type', 'deposit')"
                class="px-8 py-3 text-sm font-black rounded-xl transition-all duration-300 flex items-center gap-2"
                :class="type === 'deposit' ? 'bg-white text-blue-700 shadow-sm' : 'text-slate-400 hover:text-slate-600'">
          <span>💰 정기예금</span>
        </button>
        
        <button @click="emit('update:type', 'saving')"
                class="px-8 py-3 text-sm font-black rounded-xl transition-all duration-300 flex items-center gap-2"
                :class="type === 'saving' ? 'bg-white text-blue-700 shadow-sm' : 'text-slate-400 hover:text-slate-600'">
          <span>🌱 정기적금</span>
        </button>
      </div>
    </div>

    <div class="flex justify-center">
      <div class="inline-flex border-b-2 border-slate-100 pb-1 gap-4">
        <button v-for="s in [{id:'all', n:'전체'}, {id:'bank', n:'은행 (1금융)'}, {id:'savings', n:'저축은행 (2금융)'}]" 
                :key="s.id"
                @click="emit('update:sector', s.id)"
                :class="sector === s.id ? 'text-blue-600 font-black' : 'text-slate-400 font-bold hover:text-slate-500'"
                class="px-4 py-2 text-sm transition-colors">
          {{ s.n }}
        </button>
      </div>
    </div>

    <div class="flex flex-col lg:flex-row gap-3">
      <div class="relative lg:w-48 group">
        <select :value="bank" @change="emit('update:bank', $event.target.value)"
                class="w-full appearance-none px-5 py-4 rounded-2xl bg-slate-50 font-bold text-slate-600 outline-none transition-all cursor-pointer hover:bg-slate-100 focus:ring-2 focus:ring-blue-100 border border-transparent focus:border-blue-200">
          <option v-for="name in bankNames" :key="name" :value="name">{{ name }}</option>
        </select>
        <div class="absolute inset-y-0 right-4 flex items-center pointer-events-none text-slate-400">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/></svg>
        </div>
      </div>

      <div class="relative lg:w-40 group">
        <select :value="sort" @change="emit('update:sort', $event.target.value)"
                class="w-full appearance-none px-5 py-4 rounded-2xl bg-slate-50 font-bold text-slate-600 outline-none transition-all cursor-pointer hover:bg-slate-100 focus:ring-2 focus:ring-blue-100 border border-transparent focus:border-blue-200">
          <option value="rate">💰 금리순</option>
          <option value="name">🔡 가나다순</option>
        </select>
        <div class="absolute inset-y-0 right-4 flex items-center pointer-events-none text-slate-400">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/></svg>
        </div>
      </div>

      <div class="relative flex-1 flex gap-2">
        <div class="relative w-full">
          <div class="absolute inset-y-0 left-5 flex items-center pointer-events-none">
            <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
          <input :value="query" @input="emit('update:query', $event.target.value)"
                 type="text" placeholder="상품명이나 은행을 검색해보세요" 
                 class="w-full pl-14 pr-5 py-4 rounded-2xl bg-slate-50 font-bold text-slate-700 outline-none transition-all placeholder:text-slate-300 focus:bg-white focus:ring-4 focus:ring-blue-100 hover:bg-slate-100 border border-transparent focus:border-blue-200" />
        </div>
        
        <button class="bg-blue-600 text-white px-6 rounded-2xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-200 active:scale-95 flex items-center justify-center">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>