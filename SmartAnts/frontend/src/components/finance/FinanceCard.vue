<script setup>
defineProps(['product'])
</script>

<template>
  <div class="card bg-white border border-slate-100 hover:border-emerald-300 hover:shadow-md transition-all rounded-[2rem] p-6 cursor-pointer group">
    <div class="flex items-start justify-between mb-4">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 bg-emerald-50 rounded-2xl flex items-center justify-center text-2xl group-hover:bg-emerald-100 transition-colors">
          🏛️
        </div>
        <div>
          <h4 class="text-xs font-bold text-slate-400">{{ product.kor_co_nm }}</h4>
          <h3 class="text-lg font-black text-slate-700 group-hover:text-emerald-600 transition-colors">
            {{ product.fin_prdt_nm }}
          </h3>
        </div>
      </div>
      <div class="badge badge-ghost font-bold text-[10px] text-slate-400">
        {{ product.join_way }}
      </div>
    </div>

    <div class="grid grid-cols-2 gap-4 bg-slate-50 rounded-2xl p-4">
      <div class="text-center">
        <p class="text-[10px] text-slate-400 font-bold uppercase mb-1">기본 금리</p>
        <p class="text-xl font-black text-slate-600">{{ product.options?.[0]?.intr_rate || '-' }}%</p>
      </div>
      <div class="text-center border-l border-slate-200">
        <p class="text-[10px] text-emerald-400 font-bold uppercase mb-1">최고 금리</p>
        <p class="text-xl font-black text-emerald-500">{{ product.options?.[0]?.intr_rate2 || '-' }}%</p>
      </div>
    </div>
  </div>
</template>