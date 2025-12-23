<script setup>
defineProps({
  product: { type: Object, required: true }
})
defineEmits(['click'])
</script>

<template>
  <div @click="$emit('click')" 
       class="bg-white p-7 rounded-[2.2rem] shadow-sm border border-slate-100 hover:border-blue-500 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 cursor-pointer group flex flex-col justify-between h-full">
    <div>
      <div class="flex justify-between items-start mb-5">
        <span class="px-3 py-1.5 bg-slate-100 text-slate-500 text-[11px] font-black rounded-lg uppercase tracking-tight">
          {{ product.kor_co_nm }}
        </span>
        <span class="text-xl group-hover:scale-110 transition-transform">🐜</span>
      </div>
      <h3 class="text-xl font-black text-slate-800 leading-snug mb-2 group-hover:text-blue-600 transition-colors">
        {{ product.fin_prdt_nm }}
      </h3>
    </div>
    
    <div class="grid grid-cols-2 gap-4 border-t border-slate-50 pt-5 mt-6">
      <div>
        <p class="text-[10px] font-bold text-slate-400 mb-1 uppercase text-left tracking-wide">기본 금리</p>
        <p class="text-lg font-black text-slate-600 text-left">
          {{ product.intr_rate || '0' }}%
        </p>
      </div>
      <div class="text-right">
        <p class="text-[10px] font-bold text-blue-500 mb-1 uppercase tracking-wide">최고 금리</p>
        <p class="text-2xl font-black text-blue-600">
          {{ product.max_intr_rate || '0' }}%
        </p>
      </div>
    </div>
  </div>
</template>