<script setup>
import { ref, computed, watch, defineProps, defineEmits } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  rates: Array,
  defaultCurrency: String
})

const emit = defineEmits(['close'])

const targetCurrency = ref(props.defaultCurrency || 'USD')
const krwAmount = ref(null)
const foreignAmount = ref(null)

// 통화 기호 매핑
const getSymbol = (code) => {
  const symbols = {
    'USD': '$', 'JPY(100)': '¥', 'EUR': '€', 'CNY': '¥', 'GBP': '£',
    'AUD': 'A$', 'CAD': 'C$', 'HKD': 'HK$', 'SGD': 'S$', 'NZD': 'NZ$',
    'CHF': '₣', 'THB': '฿', 'VND': '₫', 'TWD': 'NT$', 'AED': 'Dh',
    'KRW': '₩'
  }
  return symbols[code] || ''
}

watch(() => props.isOpen, (newVal) => {
  if (newVal && props.defaultCurrency) {
    targetCurrency.value = props.defaultCurrency
  }
})

const selectedRateInfo = computed(() => props.rates.find(r => r.cur_unit === targetCurrency.value))
const realExchangeRate = computed(() => {
  if (!selectedRateInfo.value) return 0
  const rate = parseFloat(String(selectedRateInfo.value.deal_bas_r).replace(/,/g, ''))
  return selectedRateInfo.value.cur_unit.includes('(100)') ? rate / 100 : rate
})

const onKrwInput = () => {
  if (!krwAmount.value || !realExchangeRate.value) { foreignAmount.value = null; return }
  foreignAmount.value = parseFloat((krwAmount.value / realExchangeRate.value).toFixed(2))
}
const onForeignInput = () => {
  if (!foreignAmount.value || !realExchangeRate.value) { krwAmount.value = null; return }
  krwAmount.value = parseFloat((foreignAmount.value * realExchangeRate.value).toFixed(2))
}
watch(targetCurrency, onKrwInput)
const formatNumber = (num) => num ? Number(num).toLocaleString(undefined, { maximumFractionDigits: 2 }) : '0'
</script>

<template>
  <dialog class="modal backdrop-blur-md" :class="{ 'modal-open': isOpen }">
    
    <div class="modal-box bg-white rounded-3xl p-0 overflow-visible max-w-2xl shadow-2xl">
      
      <div class="bg-gray-900 text-white p-6 rounded-t-3xl flex justify-between items-center relative overflow-hidden">
        <div class="absolute -right-10 -top-10 w-40 h-40 bg-blue-500/20 rounded-full blur-3xl"></div>
        
        <h3 class="font-bold text-2xl flex items-center gap-2 z-10">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-7 h-7 text-blue-400">
            <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 21 3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
          </svg>
          환율 계산기
        </h3>
        <button @click="$emit('close')" class="btn btn-sm btn-circle btn-ghost text-white/70 hover:text-white hover:bg-white/10 z-10">✕</button>
      </div>

      <div class="p-8 space-y-6">
        
        <div class="card bg-gray-50 border border-gray-200 shadow-inner p-6 hover:border-blue-200 transition-colors group">
          <div class="flex justify-between items-center mb-2">
            <span class="font-bold text-gray-500 text-sm">대한민국 원</span>
            <div class="badge badge-neutral text-xs font-mono px-2 py-3">KRW</div>
          </div>
          <div class="flex items-center gap-3">
            <span class="text-3xl font-bold text-gray-300 group-focus-within:text-gray-900 transition-colors">₩</span>
            <input 
              type="number" 
              v-model="krwAmount" 
              @input="onKrwInput" 
              placeholder="0" 
              class="input input-ghost w-full text-4xl font-black text-right px-0 focus:bg-transparent text-gray-900 placeholder:text-gray-200" 
            />
          </div>
          <p class="text-right text-sm text-gray-400 mt-2 font-medium h-5">
            {{ krwAmount ? formatNumber(krwAmount) + ' 원' : '' }}
          </p>
        </div>

        <div class="flex justify-center -my-9 z-10 relative">
          <div class="bg-white p-2.5 rounded-full border border-gray-100 shadow-lg text-blue-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3" />
            </svg>
          </div>
        </div>

        <div class="card bg-blue-600 text-white shadow-xl p-6 relative overflow-hidden group">
          <div class="absolute -right-4 -bottom-10 w-48 h-48 bg-white/10 rounded-full blur-3xl pointer-events-none"></div>
          
          <div class="flex justify-between items-center mb-2 relative z-10">
            <span class="font-bold text-blue-100 text-sm whitespace-nowrap mr-4">환전 금액</span>
            
            <select v-model="targetCurrency" class="select select-sm select-ghost font-bold text-white focus:bg-blue-700/50 h-auto min-h-0 py-1 pl-2 pr-8 text-right border-none outline-none">
              <option v-for="rate in rates" :key="rate.id" :value="rate.cur_unit" class="text-gray-900">
                {{ rate.cur_nm }} ({{ rate.cur_unit.replace('(100)', '') }})
              </option>
            </select>
          </div>
          
          <div class="flex items-center gap-3 relative z-10">
            <span class="text-3xl font-bold text-blue-300/50">{{ getSymbol(targetCurrency) }}</span>
            <input 
              type="number" 
              v-model="foreignAmount" 
              @input="onForeignInput" 
              placeholder="0" 
              class="input input-ghost w-full text-4xl font-black text-right px-0 text-white placeholder-blue-400/30 focus:bg-transparent" 
            />
          </div>
          
          <p class="text-right text-sm text-blue-100 mt-2 font-medium h-5 relative z-10">
            {{ foreignAmount ? formatNumber(foreignAmount) : '0' }} {{ targetCurrency.replace('(100)', '') }}
          </p>
          
          <div class="divider before:bg-blue-400/50 after:bg-blue-400/50 my-4 relative z-10"></div>
          
          <p class="text-xs text-blue-100 flex justify-between items-center relative z-10">
            <span class="opacity-80">적용 환율</span>
            <span class="font-bold bg-blue-700/30 px-2 py-1 rounded">
              1 {{ targetCurrency.replace('(100)', '') }} = {{ formatNumber(realExchangeRate) }} 원
            </span>
          </p>
        </div>
      </div>

      <form method="dialog" class="modal-backdrop">
        <button @click="$emit('close')">close</button>
      </form>
    </div>
  </dialog>
</template>

<style scoped>
/* 숫자 입력 화살표 제거 */
input[type=number]::-webkit-inner-spin-button, 
input[type=number]::-webkit-outer-spin-button { 
  -webkit-appearance: none; 
  margin: 0; 
}
</style>