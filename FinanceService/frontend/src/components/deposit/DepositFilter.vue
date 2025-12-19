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
  <div class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-slate-100 space-y-8">
    <div class="flex justify-center">
      <div class="inline-flex bg-slate-100 p-1.5 rounded-2xl">
        <button v-for="s in [{id:'all', n:'전체'}, {id:'bank', n:'은행 (제1금융)'}, {id:'savings', n:'저축은행 (제2금융)'}]" 
                :key="s.id"
                @click="emit('update:sector', s.id)"
                :class="sector === s.id ? 'bg-white text-primary shadow-sm' : 'text-slate-400'"
                class="px-8 py-2.5 text-sm font-black rounded-xl transition-all">
          {{ s.n }}
        </button>
      </div>
    </div>

    <div class="flex flex-col lg:flex-row gap-4 items-center justify-between">
      <div class="flex gap-3 w-full lg:w-auto">
        <select :value="bank" @change="emit('update:bank', $event.target.value)"
                class="select select-bordered rounded-xl border-slate-200 focus:border-primary font-bold bg-slate-50 text-slate-600 flex-1 lg:w-48">
          <option v-for="name in bankNames" :key="name" :value="name">{{ name }}</option>
        </select>
        <select :value="sort" @change="emit('update:sort', $event.target.value)"
                class="select select-bordered rounded-xl border-slate-200 focus:border-primary font-bold bg-slate-50 text-slate-600 flex-1 lg:w-40">
          <option value="rate">금리 순</option>
          <option value="name">가나다 순</option>
        </select>
      </div>

      <div class="relative w-full lg:w-96">
        <span class="absolute inset-y-0 left-4 flex items-center text-primary font-bold">🔍</span>
        <input :value="query" @input="emit('update:query', $event.target.value)"
               type="text" placeholder="상품명이나 은행을 검색하세요" 
               class="input input-bordered w-full pl-12 rounded-xl border-slate-200 focus:border-primary font-bold bg-slate-50" />
      </div>
    </div>
  </div>
</template>