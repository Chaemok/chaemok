<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance'

const financeStore = useFinanceStore()

// 계산기 상태 관리
const amount = ref(1) // 입력 금액
const selectedCurrency = ref('USD') // 선택된 통화

// 🐜 선택된 통화의 실시간 환율 정보 가져오기
const currentRate = computed(() => {
  return financeStore.exchangeRates.find(r => r.cur_unit === selectedCurrency.value) || { deal_bas_r: '0', cur_nm: '정보 없음' }
})

// 🐜 계산 로직 (외화 -> 원화)
const resultKRW = computed(() => {
  const rate = parseFloat(currentRate.value.deal_bas_r.replace(/,/g, ''))
  // 일본 엔화(JPY) 등 100단위 통화 처리
  if (selectedCurrency.value.includes('(100)')) {
    return (amount.value * (rate / 100)).toLocaleString(undefined, { maximumFractionDigits: 0 })
  }
  return (amount.value * rate).toLocaleString(undefined, { maximumFractionDigits: 0 })
})

onMounted(() => {
  if (financeStore.exchangeRates.length === 0) {
    financeStore.fetchQuickData()
  }
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-10 space-y-12">
    <header class="space-y-2">
      <h2 class="text-4xl font-black text-slate-800 tracking-tight">환율 계산기 🧮</h2>
      <p class="text-slate-400 font-medium">수출입은행 실시간 데이터를 바탕으로 정확한 환율을 계산해 드립니다.</p>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
      <div class="lg:col-span-1 space-y-6">
        <div class="card bg-white shadow-xl border border-slate-100 rounded-[2.5rem] p-8 space-y-8">
          <div class="space-y-4">
            <label class="label font-bold text-slate-500 text-sm">변환할 통화 선택</label>
            <select v-model="selectedCurrency" class="select select-bordered w-full rounded-2xl border-slate-200 focus:border-primary focus:outline-none text-lg font-bold">
              <option v-for="rate in financeStore.exchangeRates" :key="rate.cur_unit" :value="rate.cur_unit">
                {{ rate.cur_nm }} ({{ rate.cur_unit }})
              </option>
            </select>
          </div>

          <div class="space-y-4">
            <label class="label font-bold text-slate-500 text-sm">금액 입력</label>
            <div class="relative">
              <input v-model.number="amount" type="number" class="input input-bordered w-full h-16 rounded-2xl border-slate-200 focus:border-primary text-2xl font-black pl-6 pr-16" />
              <span class="absolute right-6 top-1/2 -translate-y-1/2 font-bold text-slate-400">{{ selectedCurrency.split('(')[0] }}</span>
            </div>
          </div>

          <div class="divider text-slate-200">EQUALS</div>

          <div class="bg-indigo-50 rounded-3xl p-8 text-center space-y-1 border border-indigo-100">
            <p class="text-xs font-bold text-primary uppercase tracking-widest">대한민국 원 (KRW)</p>
            <p class="text-4xl font-black text-slate-800">{{ resultKRW }}원</p>
          </div>
        </div>

        <div class="bg-slate-800 text-white p-6 rounded-[2rem] shadow-lg relative overflow-hidden">
          <p class="text-sm opacity-80 leading-relaxed relative z-10">
            실시간 매매기준율 기준이며,<br />
            은행별 환전 수수료에 따라<br />
            실제 환전 금액은 다를 수 있습니다.
          </p>
          <div class="absolute -right-4 -bottom-4 text-6xl opacity-20">🐜</div>
        </div>
      </div>

      <div class="lg:col-span-2">
        <div class="card bg-white shadow-sm border border-slate-100 rounded-[2.5rem] overflow-hidden">
          <div class="p-8 border-b border-slate-50 flex justify-between items-center">
            <h3 class="text-xl font-bold text-slate-800">실시간 매매기준율</h3>
            <span class="text-xs font-bold text-slate-400">데이터 제공: 한국수출입은행</span>
          </div>
          
          <div class="overflow-x-auto">
            <table class="table w-full">
              <thead class="bg-slate-50 text-slate-400">
                <tr>
                  <th class="py-4 pl-8">통화명</th>
                  <th>매매기준율</th>
                  <th>전일대비</th>
                  <th class="pr-8 text-right">송금 보낼 때</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="financeStore.isMainLoading" v-for="n in 5" :key="n" class="animate-pulse">
                  <td colspan="4" class="p-4"><div class="h-10 bg-slate-50 rounded-xl w-full"></div></td>
                </tr>
                <tr v-else v-for="rate in financeStore.exchangeRates" :key="rate.cur_unit" 
                    @click="selectedCurrency = rate.cur_unit"
                    class="hover:bg-indigo-50/50 transition-colors cursor-pointer border-b border-slate-50 last:border-none group">
                  <td class="py-5 pl-8">
                    <div class="flex items-center gap-3">
                      <div class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-sm group-hover:bg-white transition-colors">🌎</div>
                      <div>
                        <p class="font-bold text-slate-700">{{ rate.cur_nm }}</p>
                        <p class="text-[10px] text-slate-400 uppercase">{{ rate.cur_unit }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="font-black text-slate-700 text-lg">{{ rate.deal_bas_r }}</td>
                  <td>
                    <span class="text-xs font-bold text-primary">변동없음</span>
                  </td>
                  <td class="pr-8 text-right font-medium text-slate-500">{{ rate.tts }}원</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 입력 필드 숫자 화살표 제거 */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>