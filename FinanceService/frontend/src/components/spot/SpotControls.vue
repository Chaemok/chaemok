<script setup>
defineProps({
  startDate: String,
  endDate: String,
  selectedAsset: String
})

const emit = defineEmits(['update:startDate', 'update:endDate', 'update:selectedAsset', 'search'])
</script>

<template>
  <div class="bg-white rounded-[2rem] p-6 shadow-xl shadow-slate-200/50 mb-8 border border-slate-100 flex flex-col md:flex-row items-center justify-between gap-6">
    
    <div class="flex items-center gap-3 bg-slate-50 p-3 rounded-2xl border border-slate-200">
      <input 
        type="date" 
        :value="startDate" 
        @input="$emit('update:startDate', $event.target.value)"
        class="bg-transparent font-bold text-slate-600 focus:outline-none cursor-pointer" 
      />
      <span class="text-slate-400 font-bold">~</span>
      <input 
        type="date" 
        :value="endDate" 
        @input="$emit('update:endDate', $event.target.value)"
        class="bg-transparent font-bold text-slate-600 focus:outline-none cursor-pointer" 
      />
      <button 
        @click="$emit('search')" 
        class="ml-2 bg-slate-900 text-white px-5 py-2 rounded-xl font-bold hover:bg-blue-600 transition-colors shadow-lg active:scale-95"
      >
        조회
      </button>
    </div>

    <div class="flex bg-slate-100 p-1.5 rounded-2xl">
      <button 
        @click="$emit('update:selectedAsset', 'GOLD')" 
        class="px-8 py-3 rounded-xl font-black transition-all text-sm"
        :class="selectedAsset === 'GOLD' ? 'bg-white text-yellow-600 shadow-md transform scale-105' : 'text-slate-400 hover:text-slate-600'"
      >
        GOLD (금)
      </button>
      <button 
        @click="$emit('update:selectedAsset', 'SILVER')" 
        class="px-8 py-3 rounded-xl font-black transition-all text-sm"
        :class="selectedAsset === 'SILVER' ? 'bg-white text-slate-600 shadow-md transform scale-105' : 'text-slate-400 hover:text-slate-600'"
      >
        SILVER (은)
      </button>
    </div>
  </div>
</template>