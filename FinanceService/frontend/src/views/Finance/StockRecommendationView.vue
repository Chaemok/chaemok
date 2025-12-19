<script setup>
import { ref, onMounted, reactive } from 'vue'
import axios from 'axios'
// 🐜 [수정] user -> auth 스토어로 변경
import { useAuthStore } from '@/stores/auth' 
import { useFinanceStore } from '@/stores/finance'
import PageHeader from '@/components/common/PageHeader.vue'

const authStore = useAuthStore() // 🐜 명칭 변경
const financeStore = useFinanceStore()

const loading = ref(true)
const stocks = ref([])
const baseDate = ref('')

// 사용자 투자 성향
const userProfile = reactive({
  investment_style: 'balanced'
})

// 성향별 가중치 정의 (동일)
const weightMap = {
  stable:     { w_div: 0.60, w_roe: 0.20, w_per: 0.10, w_pbr: 0.10 },
  balanced:   { w_div: 0.30, w_roe: 0.40, w_per: 0.15, w_pbr: 0.15 },
  aggressive: { w_div: 0.00, w_roe: 0.50, w_per: 0.30, w_pbr: 0.20 }
}

const styles = [
  { label: '안정형', value: 'stable', icon: '🛡️', desc: '고배당주 중심의 안전한 투자' },
  { label: '균형형', value: 'balanced', icon: '⚖️', desc: '수익성과 저평가의 적절한 조화' },
  { label: '공격형', value: 'aggressive', icon: '🔥', desc: '높은 ROE와 성장성 위주의 투자' },
]

// 1. 데이터 가져오기
const fetchData = async () => {
  loading.value = true
  const currentWeights = weightMap[userProfile.investment_style]

  try {
    // 🐜 [수정] authStore의 토큰과 로그인 상태 확인 (isLoggedIn 사용)
    const headers = authStore.isLoggedIn ? { Authorization: `Token ${authStore.token}` } : {}
    
    const res = await axios.get(`${financeStore.API_URL}/api/finlife/stocks/recommend/`, {
      headers: headers,
      params: currentWeights 
    })
    
    if (res.data.rows) {
      stocks.value = res.data.rows
      baseDate.value = res.data.base_date
    } else {
      stocks.value = res.data
    }
  } catch (err) {
    console.error("데이터 로딩 실패:", err)
  } finally {
    loading.value = false
  }
}

// 2. 분석 실행 핸들러
const handleAnalyze = async () => {
  // 🐜 [수정] authStore.isLoggedIn으로 체크
  if (authStore.isLoggedIn) {
    try {
      await axios.put(`${financeStore.API_URL}/api/accounts/profile/preference/`, {
        investment_style: userProfile.investment_style,
      }, { headers: { Authorization: `Token ${authStore.token}` } })
    } catch (e) {
      console.warn("성향 저장 실패 (무시하고 분석 진행)", e)
    }
  }
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 pb-20">
    <div class="max-w-7xl mx-auto px-4 py-12 space-y-10">
      
      <PageHeader 
        title="📈 맞춤 주식 추천" 
        subtitle="투자 성향에 따른 가중치를 적용하여 스마트 개미들을 위한 최적의 종목을 분석합니다. 🐜" 
      />

      <div class="max-w-4xl mx-auto">
        <div class="bg-white rounded-[2.5rem] shadow-xl shadow-indigo-100/50 p-8 md:p-10 border border-slate-100">
          <h3 class="text-xl font-black text-slate-800 mb-8 flex items-center gap-2">
            🎯 나만의 투자 전략 설정
          </h3>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
            <label v-for="style in styles" :key="style.value" 
                   class="relative cursor-pointer group">
              <input type="radio" :value="style.value" v-model="userProfile.investment_style" class="hidden peer">
              <div class="h-full border-2 border-slate-100 rounded-[2rem] p-6 flex flex-col items-center text-center transition-all 
                          peer-checked:border-indigo-500 peer-checked:bg-indigo-50/30 peer-checked:ring-4 peer-checked:ring-indigo-50
                          group-hover:border-indigo-200">
                <span class="text-4xl mb-4 transition-transform group-hover:scale-110">{{ style.icon }}</span>
                <span class="text-lg font-black text-slate-800 mb-2">{{ style.label }}</span>
                <p class="text-xs text-slate-400 font-medium leading-relaxed">{{ style.desc }}</p>
              </div>
              <div class="absolute top-4 right-4 opacity-0 peer-checked:opacity-100 transition-opacity">
                <div class="bg-indigo-500 text-white rounded-full p-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </div>
              </div>
            </label>
          </div>

          <button @click="handleAnalyze" 
                  class="w-full py-5 bg-indigo-600 text-white text-lg font-black rounded-2xl shadow-lg shadow-indigo-200 hover:bg-indigo-700 hover:-translate-y-0.5 transition-all active:scale-[0.98]">
            선택한 전략으로 종목 다시 분석하기 🐜🚀
          </button>
        </div>
      </div>

      <div class="bg-white rounded-[2.5rem] shadow-xl shadow-slate-200/50 overflow-hidden border border-slate-100">
        <div class="p-8 border-b border-slate-50 flex flex-col md:flex-row justify-between items-center gap-6">
          <div class="flex items-center gap-4">
            <h3 class="text-2xl font-black text-slate-800">📊 맞춤 추천 랭킹</h3>
            <span v-if="baseDate" class="px-3 py-1 bg-slate-100 text-slate-400 text-[10px] font-bold rounded-full uppercase tracking-wider">
              {{ baseDate }} 기준
            </span>
          </div>
          <button @click="fetchData" class="flex items-center gap-2 px-5 py-2.5 bg-slate-50 text-slate-500 font-bold rounded-xl hover:bg-slate-100 transition-colors border border-slate-100">
            <span :class="{ 'animate-spin': loading }">🔄</span> 새로고침
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full border-collapse">
            <thead>
              <tr class="bg-slate-50/50 text-slate-400 text-[11px] font-black uppercase tracking-[0.2em]">
                <th class="py-5 pl-10 text-left w-20">순위</th>
                <th class="py-5 text-left">종목명</th>
                <th class="py-5 text-center">종합점수</th>
                <th class="py-5 text-right">배당률</th>
                <th class="py-5 text-right">ROE</th>
                <th class="py-5 text-right">PER</th>
                <th class="py-5 text-right">PBR</th>
                <th class="py-5 pr-10 text-center">섹터</th>
              </tr>
            </thead>
            
            <tbody class="divide-y divide-slate-50">
              <tr v-if="loading">
                <td colspan="8" class="text-center py-32">
                  <span class="loading loading-spinner loading-lg text-indigo-600"></span>
                  <p class="mt-4 text-slate-400 font-bold">AI가 최적의 종목을 선별 중입니다... 🐜</p>
                </td>
              </tr>
              <tr v-else-if="stocks.length === 0">
                <td colspan="8" class="text-center py-32 text-slate-400 font-bold">
                  추천할 종목이 없습니다. 전략을 다시 선택해보세요. 😳
                </td>
              </tr>
              <tr v-else v-for="(stock, index) in stocks" :key="stock.ticker" 
                  class="hover:bg-indigo-50/30 transition-colors group cursor-pointer">
                <td class="py-6 pl-10">
                  <span :class="index < 3 ? 'text-indigo-600 font-black' : 'text-slate-400 font-bold'" class="text-xl">
                    {{ index + 1 }}
                  </span>
                </td>
                <td class="py-6">
                  <div class="flex flex-col">
                    <span class="text-base font-black text-slate-800 group-hover:text-indigo-600 transition-colors">{{ stock.name }}</span>
                    <span class="text-[10px] text-slate-400 font-bold tracking-widest">{{ stock.ticker }}</span>
                  </div>
                </td>
                <td class="py-6 text-center">
                  <span class="px-4 py-1.5 bg-indigo-50 text-indigo-600 font-black rounded-full text-sm">
                    {{ stock.score }}점
                  </span>
                </td>
                <td class="py-6 text-right font-black text-rose-500">{{ stock.DIV }}%</td>
                <td class="py-6 text-right font-bold text-slate-600">{{ stock.ROE_est ? stock.ROE_est.toFixed(2) : '-' }}%</td>
                <td class="py-6 text-right font-bold text-slate-600">{{ stock.PER }}</td>
                <td class="py-6 text-right font-bold text-slate-600">{{ stock.PBR }}</td>
                <td class="py-6 pr-10 text-center">
                  <span class="bg-slate-100 text-slate-500 px-3 py-1 rounded-lg text-[10px] font-black uppercase">{{ stock.Sector }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="p-8 bg-slate-50/50 text-center border-t border-slate-50">
          <p class="text-xs text-slate-400 font-bold flex items-center justify-center gap-2">
             🐜 분석 결과는 투자 참고용일 뿐이며, 모든 투자 책임은 본인에게 있습니다. (Data: FinanceDataReader)
          </p>
        </div>
      </div>
    </div>
  </div>
</template>