<script setup>
defineProps({
  startDate: String,
  endDate: String,
  selectedAsset: String
})

const emit = defineEmits(['update:startDate', 'update:endDate', 'update:selectedAsset', 'search'])
</script>

<template>
  <div class="bg-white rounded-[2rem] p-6 shadow-xl shadow-slate-200/50 mb-8 border border-slate-100 flex flex-wrap md:flex-nowrap items-center justify-between gap-4">
    
    <div class="flex items-center gap-2 bg-slate-50 p-2 rounded-2xl border border-slate-200 w-full md:w-auto overflow-x-auto">
      <input 
        type="date" 
        :value="startDate" 
        @input="$emit('update:startDate', $event.target.value)"
        class="bg-transparent font-bold text-slate-600 focus:outline-none cursor-pointer text-xs md:text-sm p-1" 
      />
      <span class="text-slate-400 font-bold">~</span>
      <input 
        type="date" 
        :value="endDate" 
        @input="$emit('update:endDate', $event.target.value)"
        class="bg-transparent font-bold text-slate-600 focus:outline-none cursor-pointer text-xs md:text-sm p-1" 
      />
      <button 
        @click="$emit('search')" 
        class="ml-1 bg-slate-900 text-white px-4 py-2 rounded-xl font-bold hover:bg-blue-600 transition-colors shadow-lg active:scale-95 whitespace-nowrap shrink-0 text-xs md:text-sm"
      >
        조회
      </button>
    </div>

    <div class="flex bg-slate-100 p-1.5 rounded-2xl w-full md:w-auto">
      <button 
        @click="$emit('update:selectedAsset', 'GOLD')" 
        class="flex-1 md:flex-none px-6 py-3 rounded-xl font-black transition-all text-sm whitespace-nowrap"
        :class="selectedAsset === 'GOLD' ? 'bg-white text-yellow-600 shadow-md transform scale-105' : 'text-slate-400 hover:text-slate-600'"
      >
        GOLD (금)
      </button>
      <button 
        @click="$emit('update:selectedAsset', 'SILVER')" 
        class="flex-1 md:flex-none px-6 py-3 rounded-xl font-black transition-all text-sm whitespace-nowrap"
        :class="selectedAsset === 'SILVER' ? 'bg-white text-slate-600 shadow-md transform scale-105' : 'text-slate-400 hover:text-slate-600'"
      >
        SILVER (은)
      </button>
    </div>
  </div>
</template>