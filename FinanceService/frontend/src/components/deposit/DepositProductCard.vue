<script setup>
defineProps({
  product: { type: Object, required: true }
})
// 부모에게 클릭되었음을 알리는 emit 설정
defineEmits(['click'])
</script>

<template>
  <div @click="$emit('click')" 
       class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-slate-50 hover:border-indigo-500 hover:shadow-xl hover:-translate-y-1 transition-all cursor-pointer group flex flex-col justify-between h-full">
    <div>
      <div class="flex justify-between items-start mb-4">
        <span class="px-3 py-1 bg-slate-100 text-slate-500 text-[10px] font-black rounded-lg uppercase">
          {{ product.kor_co_nm }}
        </span>
        <span class="text-xl group-hover:scale-110 transition-transform">🐜</span>
      </div>
      <h3 class="text-xl font-black text-slate-800 leading-tight mb-6 group-hover:text-indigo-600 transition-colors">
        {{ product.fin_prdt_nm }}
      </h3>
    </div>
    
    <div class="grid grid-cols-2 gap-4 border-t border-slate-50 pt-6">
      <div>
        <p class="text-[10px] font-bold text-slate-300 mb-1 uppercase text-left">기본 금리</p>
        <p class="text-lg font-black text-slate-700 text-left">
          {{ product.intr_rate || '0' }}%
        </p>
      </div>
      <div class="text-right">
        <p class="text-[10px] font-bold text-indigo-500 mb-1 uppercase">최고 금리</p>
        <p class="text-2xl font-black text-indigo-600">
          {{ product.max_intr_rate || '0' }}%
        </p>
      </div>
    </div>
  </div>
</template>