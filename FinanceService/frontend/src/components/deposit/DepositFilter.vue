<script setup>
const props = defineProps({
  sector: String,
  bank: String,
  query: String,
  sort: String,
  bankNames: Array
})

const emit = defineEmits(['update:sector', 'update:bank', 'update:query', 'update:sort'])
</script>

<template>
  <div class="bg-white p-8 rounded-[2.5rem] shadow-xl shadow-blue-500/5 border border-blue-50 space-y-8">
    
    <div class="flex justify-center">
      <div class="inline-flex bg-blue-50/50 p-1.5 rounded-2xl border border-blue-100">
        <button v-for="s in [{id:'all', n:'전체'}, {id:'bank', n:'은행 (1금융)'}, {id:'savings', n:'저축은행 (2금융)'}]" 
                :key="s.id"
                @click="emit('update:sector', s.id)"
                :class="sector === s.id 
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-600/20' 
                  : 'text-slate-500 hover:text-blue-600 hover:bg-blue-100/50'"
                class="px-6 md:px-8 py-3 text-sm font-black rounded-xl transition-all duration-300">
          {{ s.n }}
        </button>
      </div>
    </div>

    <div class="flex flex-col lg:flex-row gap-4 items-center justify-between">
      <div class="flex gap-3 w-full lg:w-auto">
        <div class="relative flex-1 lg:w-48 group">
          <select :value="bank" @change="emit('update:bank', $event.target.value)"
                  class="w-full appearance-none px-5 py-4 rounded-2xl border-2 border-slate-100 bg-white font-bold text-slate-600 outline-none transition-all
                         focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 group-hover:border-blue-200">
            <option v-for="name in bankNames" :key="name" :value="name">{{ name }}</option>
          </select>
          <div class="absolute inset-y-0 right-4 flex items-center pointer-events-none text-slate-400 group-hover:text-blue-500 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/></svg>
          </div>
        </div>

        <div class="relative flex-1 lg:w-40 group">
          <select :value="sort" @change="emit('update:sort', $event.target.value)"
                  class="w-full appearance-none px-5 py-4 rounded-2xl border-2 border-slate-100 bg-white font-bold text-slate-600 outline-none transition-all
                         focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 group-hover:border-blue-200">
            <option value="rate">💰 금리순</option>
            <option value="name">🔡 가나다순</option>
          </select>
          <div class="absolute inset-y-0 right-4 flex items-center pointer-events-none text-slate-400 group-hover:text-blue-500 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/></svg>
          </div>
        </div>
      </div>

      <div class="relative w-full lg:w-96 group">
        <div class="absolute inset-y-0 left-5 flex items-center pointer-events-none">
          <svg class="w-5 h-5 text-slate-400 group-focus-within:text-blue-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
        <input :value="query" @input="emit('update:query', $event.target.value)"
               type="text" placeholder="상품명이나 은행을 찾아보세요" 
               class="w-full pl-14 pr-5 py-4 rounded-2xl border-2 border-slate-100 bg-white font-bold text-slate-700 outline-none transition-all
                      placeholder:text-slate-300 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 group-hover:border-blue-200" />
      </div>
    </div>
  </div>
</template>