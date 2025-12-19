<script setup>
import { useFinanceStore } from '@/stores/finance'
const store = useFinanceStore()
</script>

<template>
  <section class="mb-12">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-2xl font-black text-slate-800">채목님을 위한 맞춤 상품 💎</h3>
      <router-link to="/finance" class="text-sm font-bold text-emerald-600">더보기</router-link>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="n in 2" :key="n" class="card card-side bg-white shadow-sm border border-slate-100 rounded-[2rem] hover:border-emerald-200 transition-all cursor-pointer overflow-hidden">
        <figure class="w-1/3 bg-indigo-50 flex items-center justify-center text-4xl">
          🏛️
        </figure>
        <div class="card-body p-6">
          <div class="badge badge-outline badge-sm text-slate-400">정기예금</div>
          <h2 class="card-title text-slate-700 font-bold">신한 My플러스 정기예금</h2>
          <p class="text-xs text-slate-400">최고 연 <span class="text-emerald-500 font-bold text-lg">4.0%</span></p>
          <div class="card-actions justify-end">
            <button class="btn btn-ghost btn-sm text-emerald-600">자세히 보기</button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>