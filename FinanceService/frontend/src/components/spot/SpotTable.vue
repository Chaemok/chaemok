<script setup>
import { computed } from 'vue'

const props = defineProps({
  historyData: { type: Array, default: () => [] }
})

// 최신순 정렬 (차트는 과거->미래, 표는 미래->과거가 보기 편함)
const sortedData = computed(() => [...props.historyData].reverse())

const formatNum = (n) => Number(n).toLocaleString()
</script>

<template>
  <div class="mt-8 bg-white rounded-[2rem] border border-slate-100 shadow-lg overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full text-sm text-center">
        <thead class="bg-slate-50 border-b border-slate-100 text-slate-500">
          <tr>
            <th class="py-4 font-black">날짜</th>
            <th class="py-4 font-black">원화 시세 (KRW)</th>
            <th class="py-4 font-black">국제 시세 (USD)</th>
            <th class="py-4 font-black">전일 대비</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-50">
          <tr v-for="(row, index) in sortedData" :key="row.date" class="hover:bg-slate-50/50 transition-colors">
            <td class="py-3 font-bold text-slate-600">{{ row.date }}</td>
            <td class="py-3 font-black text-slate-800">{{ formatNum(row.rate_krw) }}원</td>
            <td class="py-3 font-medium text-slate-500">${{ formatNum(row.rate_usd) }}</td>
            <td class="py-3 font-bold">
              <span v-if="index < sortedData.length - 1">
                 <span v-if="row.rate_krw > sortedData[index+1].rate_krw" class="text-red-500">
                   ▲ {{ formatNum(row.rate_krw - sortedData[index+1].rate_krw) }}
                 </span>
                 <span v-else-if="row.rate_krw < sortedData[index+1].rate_krw" class="text-blue-500">
                   ▼ {{ formatNum(sortedData[index+1].rate_krw - row.rate_krw) }}
                 </span>
                 <span v-else class="text-slate-400">-</span>
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-if="historyData.length === 0" class="p-10 text-center text-slate-400 font-bold">
      표시할 데이터가 없습니다.
    </div>
  </div>
</template>