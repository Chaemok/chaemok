<script setup>
defineProps({
  products: Array,
  type: String // '예금' or '적금'
})
</script>

<template>
  <div class="space-y-4">
    <h3 class="text-lg font-black text-slate-800 flex items-center gap-2">
      <span class="text-xl">{{ type === '예금' ? '💰' : '🐖' }}</span> 가입한 {{ type }}
    </h3>
    
    <div v-if="products.length > 0" class="grid gap-3">
      <div v-for="item in products" :key="item.id" 
           class="p-5 bg-white border border-slate-100 rounded-2xl shadow-sm hover:shadow-md transition-all flex justify-between items-center group">
        <div>
          <span class="text-[10px] font-bold text-slate-400 block mb-1">{{ item.product.kor_co_nm }}</span>
          <h4 class="font-black text-slate-800 group-hover:text-blue-600 transition-colors">
            {{ item.product.fin_prdt_nm }}
          </h4>
        </div>
        <div class="text-right">
          <span class="text-xs font-bold text-slate-400">최고 금리</span>
          <p class="text-lg font-black text-blue-600">{{ item.intr_rate2 }}%</p>
        </div>
      </div>
    </div>

    <div v-else class="p-8 bg-slate-50 rounded-2xl border border-dashed border-slate-200 text-center text-slate-400 font-bold text-sm">
      가입한 {{ type }} 상품이 없습니다.
    </div>
  </div>
</template>