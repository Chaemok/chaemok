<script setup>
// 부모(HomeView)로부터 데이터를 받도록 선언
defineProps({
  stocks: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <div class="sa-card overflow-hidden">
    <div class="p-8 pb-4 flex justify-between items-center">
      <h3 class="text-xl font-bold text-slate-800">Smart Ants 퀀트 랭킹 🐜</h3>
      <div v-if="isLoading" class="badge badge-ghost animate-pulse text-xs">데이터 로드 중...</div>
    </div>

    <div class="px-2 pb-6">
      <div v-if="isLoading" class="p-6 space-y-4">
        <div v-for="n in 5" :key="n" class="h-12 w-full bg-slate-50 animate-pulse rounded-xl"></div>
      </div>

      <table v-else class="table w-full">
        <thead>
          <tr class="text-slate-400 border-none">
            <th>순위</th>
            <th>종목명</th>
            <th>배당률</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(stock, idx) in stocks" :key="idx" class="hover:bg-indigo-50/50 border-none transition-colors">
            <td class="font-bold text-primary">{{ idx + 1 }}</td>
            <td class="font-bold text-slate-700">{{ stock.name || '종목명 없음' }}</td>
            <td class="text-slate-500">{{ stock.DIV || 0 }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>