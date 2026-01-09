<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  rates: { type: Array, default: () => [] }
})

const amount = ref(1)
const fromCurrency = ref('USD')
const toCurrency = ref('KRW')

// 🔧 안전한 숫자 변환 함수
const parseRate = (value) => {
  if (!value) return 0
  if (typeof value === 'number') return value
  return parseFloat(value.toString().replace(/,/g, ''))
}

// 필드명 안전하게 찾기
const getRateValue = (rateObj) => {
  if (!rateObj) return 0
  return parseRate(rateObj.kftc_deal_bas_r || rateObj.deal_bas_r || rateObj.tts)
}

// 옵션 리스트 생성
const currencyOptions = computed(() => {
  const options = props.rates.map(rate => ({
    code: rate.cur_unit,
    name: rate.cur_nm
  }))

  const hasKRW = options.some(o => o.code === 'KRW')
  if (!hasKRW) options.unshift({ code: 'KRW', name: '한국 원' })

  const hasUSD = options.some(o => o.code === 'USD')
  if (!hasUSD) options.unshift({ code: 'USD', name: '미국 달러' })
  
  const uniqueOptions = []
  const seenCodes = new Set()
  options.forEach(opt => {
    if (!seenCodes.has(opt.code)) {
      seenCodes.add(opt.code)
      uniqueOptions.push(opt)
    }
  })
  return uniqueOptions
})

// 환율 계산 로직
const convertedAmount = computed(() => {
  let fromRate = 1
  let toRate = 1

  if (fromCurrency.value !== 'KRW') {
    const fromData = props.rates.find(r => r.cur_unit === fromCurrency.value)
    fromRate = getRateValue(fromData)
  }

  if (toCurrency.value !== 'KRW') {
    const toData = props.rates.find(r => r.cur_unit === toCurrency.value)
    toRate = getRateValue(toData)
  }

  if (toRate === 0) return 0
  const valInKRW = amount.value * fromRate
  return (valInKRW / toRate).toFixed(2)
})

const formatNumber = (num) => {
  return Number(num).toLocaleString(undefined, { maximumFractionDigits: 2 })
}
</script>

<template>
  <div class="bg-white rounded-[2rem] p-6 md:p-8 shadow-xl shadow-blue-500/5 border border-blue-50 relative overflow-visible">
    <div class="absolute top-0 right-0 w-64 h-64 bg-blue-50 rounded-full blur-3xl -z-10 translate-x-1/3 -translate-y-1/3 opacity-70"></div>
    
    <div class="grid grid-cols-1 md:grid-cols-[1fr_auto_1fr] gap-4 md:gap-8 items-end">
      
      <div class="w-full space-y-2">
        <label class="text-sm font-bold text-slate-500 ml-2">환전할 금액</label>
        <div class="flex items-center bg-slate-50 p-2 rounded-2xl border border-slate-200 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 transition-all">
          <input 
            type="number" 
            v-model="amount" 
            min="0" 
            class="bg-transparent text-2xl font-black text-slate-800 p-2 w-full focus:outline-none text-right min-w-0" 
            placeholder="0"
          />
          <div class="w-px h-6 bg-slate-300 mx-2"></div>
          
          <select v-model="fromCurrency" class="bg-transparent text-sm font-bold text-blue-600 p-2 focus:outline-none cursor-pointer min-w-[120px] max-w-[160px] truncate">
            <option v-for="opt in currencyOptions" :key="opt.code" :value="opt.code">
              {{ opt.code }} ({{ opt.name }})
            </option>
          </select>
        </div>
      </div>

      <div class="flex justify-center md:pb-3">
        <div class="w-12 h-12 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </div>
      </div>

      <div class="w-full space-y-2">
        <label class="text-sm font-bold text-slate-500 ml-2">환전 결과</label>
        <div class="flex items-center bg-blue-600/5 p-2 rounded-2xl border border-blue-100">
          <input 
            type="text" 
            :value="formatNumber(convertedAmount)" 
            readonly 
            class="bg-transparent text-2xl font-black text-blue-600 p-2 w-full focus:outline-none text-right pointer-events-none min-w-0" 
          />
          <div class="w-px h-6 bg-blue-200 mx-2"></div>
          
          <select v-model="toCurrency" class="bg-transparent text-sm font-bold text-blue-700 p-2 focus:outline-none cursor-pointer min-w-[120px] max-w-[160px] truncate">
            <option v-for="opt in currencyOptions" :key="opt.code" :value="opt.code">
              {{ opt.code }} ({{ opt.name }})
            </option>
          </select>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
</style>