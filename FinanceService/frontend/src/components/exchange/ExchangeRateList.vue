<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  rates: { type: Array, default: () => [] }
})

const emit = defineEmits(['item-click'])

const sortMode = ref('major')
const majorCurrencies = ['USD', 'EUR', 'JPY(100)', 'CNH', 'HKD', 'GBP', 'AUD', 'CAD']

const sortedRates = computed(() => {
  let list = props.rates.filter(rate => rate.cur_unit !== 'KRW')
  
  if (sortMode.value === 'major') {
    list.sort((a, b) => {
      const aIsMajor = majorCurrencies.includes(a.cur_unit)
      const bIsMajor = majorCurrencies.includes(b.cur_unit)
      if (aIsMajor && bIsMajor) return majorCurrencies.indexOf(a.cur_unit) - majorCurrencies.indexOf(b.cur_unit)
      if (aIsMajor) return -1
      if (bIsMajor) return 1
      return a.cur_unit.localeCompare(b.cur_unit)
    })
  } else {
    list.sort((a, b) => a.cur_unit.localeCompare(b.cur_unit))
  }
  return list
})

const parseRate = (value) => {
  if (!value) return 0
  if (typeof value === 'number') return value
  const cleanStr = value.toString().replace(/,/g, '')
  const num = parseFloat(cleanStr)
  return isNaN(num) ? 0 : num
}

const formatNumber = (val) => {
  const num = parseRate(val)
  if (num === 0) return '-'
  return num.toLocaleString(undefined, { maximumFractionDigits: 2 })
}

const getBase = (rate) => rate.kftc_deal_bas_r || rate.deal_bas_r || 0

const getFlagUrl = (currencyCode) => {
  if (!currencyCode) return ''
  let code = currencyCode.substring(0, 2).toLowerCase()
  if (currencyCode === 'EUR') code = 'eu'
  if (currencyCode === 'JPY') code = 'jp'
  if (currencyCode === 'CNH') code = 'cn'
  return `https://flagcdn.com/w40/${code}.png`
}
</script>

<template>
  <div class="bg-white rounded-[2rem] shadow-lg border border-slate-100 overflow-hidden">
    
    <div class="px-6 py-4 border-b border-slate-100 flex justify-end bg-slate-50/50">
      <select 
        v-model="sortMode" 
        class="bg-white border border-slate-200 text-slate-600 text-sm font-bold rounded-lg px-3 py-2 focus:outline-none focus:border-blue-500 cursor-pointer shadow-sm"
      >
        <option value="major">⭐ 주요 통화순</option>
        <option value="abc">🔤 ABC순</option>
      </select>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full text-left whitespace-nowrap">
        <thead class="bg-slate-50 border-b border-slate-100">
          <tr>
            <th class="py-4 px-6 text-sm font-black text-slate-500">통화</th>
            <th class="py-4 px-6 text-sm font-black text-slate-500 text-right">매매기준율</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-50">
          <tr v-for="rate in sortedRates" :key="rate.cur_unit" 
              @click="emit('item-click', rate)"
              class="hover:bg-blue-50/50 transition-colors cursor-pointer group">
            
            <td class="py-5 px-6">
              <div class="flex items-center gap-4">
                <img :src="getFlagUrl(rate.cur_unit)" alt="flag" class="w-10 h-10 rounded-full shadow-sm object-cover border border-slate-100 group-hover:scale-110 transition-transform" />
                <div>
                  <div class="font-black text-slate-800 text-base">{{ rate.cur_unit }}</div>
                  <div class="text-xs font-bold text-slate-400 mt-0.5">{{ rate.cur_nm }}</div>
                </div>
              </div>
            </td>
            
            <td class="py-5 px-6 text-right font-black text-xl text-blue-600">
              {{ formatNumber(getBase(rate)) }}
              <span class="text-xs text-slate-400 font-normal ml-1">KRW</span>
            </td>

          </tr>
          
          <tr v-if="sortedRates.length === 0">
            <td colspan="2" class="py-10 text-center text-slate-400 font-bold">
              표시할 환율 정보가 없습니다.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>