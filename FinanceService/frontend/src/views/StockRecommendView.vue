<script setup>
import { ref, onMounted, reactive } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useFinanceStore } from '@/stores/finance'
import PageHeader from '@/components/layout/PageHeader.vue'
import BaseCard from '@/components/BaseCard.vue' // BaseCard 경로에 맞게 수정 필요

const userStore = useUserStore()
const financeStore = useFinanceStore()

const loading = ref(true)
const stocks = ref([])
const baseDate = ref('')

// 사용자 입력 데이터
const userProfile = reactive({
  investment_style: 'balanced', // 기본값: 균형형
  preferred_products: [] 
})

// ✨ [핵심] 성향별 가중치 정의
const weightMap = {
  // 배당(DIV) + 저PBR(PBR) 집중
  stable:     { w_div: 0.60, w_roe: 0.20, w_per: 0.10, w_pbr: 0.10 }, 
  // ROE + 밸런스
  balanced:   { w_div: 0.30, w_roe: 0.40, w_per: 0.15, w_pbr: 0.15 }, 
  // ROE + 저PER/PBR (성장성 + 저평가) 집중, 배당은 0
  aggressive: { w_div: 0.00, w_roe: 0.50, w_per: 0.30, w_pbr: 0.20 }  
}


const styles = [
  { label: '안정형', value: 'stable', icon: '🛡️' },
  { label: '균형형', value: 'balanced', icon: '⚖️' },
  { label: '공격형', value: 'aggressive', icon: '🔥' },
]

// 1. 데이터 가져오기 (가중치 파라미터 추가)
const fetchData = async () => {
  loading.value = true
  
  // 현재 선택된 스타일에 맞는 가중치 가져오기
  const currentWeights = weightMap[userProfile.investment_style]

  try {
    const headers = userStore.token ? { Authorization: `Bearer ${userStore.token}` } : {}
    
    // ✨ params에 가중치 실어 보내기
    const res = await axios.get(`${financeStore.API_URL}/api/finances/stocks/recommend/`, {
      headers: headers,
      params: currentWeights // { w_div: 0.6, ... } 형태로 쿼리스트링 전송
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

// 2. 버튼 클릭 핸들러 (저장 대신 즉시 분석)
const handleAnalyze = async () => {
  // 로그인 상태면 성향 저장도 같이 해줌 (UX 향상)
  if (userStore.isLogin) {
    try {
      await axios.put(`${financeStore.API_URL}/api/accounts/profile/preference/`, {
        investment_style: userProfile.investment_style,
        preferred_products: userProfile.preferred_products
      }, { headers: { Authorization: `Bearer ${userStore.token}` } })
    } catch (e) {
      console.warn("성향 저장 실패 (무시하고 분석 진행)", e)
    }
  }

  // 변경된 성향으로 데이터 다시 가져오기
  const selectedStyleLabel = styles.find(s => s.value === userProfile.investment_style).label
  alert(`'${selectedStyleLabel}' 전략으로 종목을 다시 분석합니다! 🔄`)
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-10 min-h-screen">
    
    <PageHeader 
      title="📈 맞춤 주식 추천" 
      subtitle="투자 성향을 선택하면 가중치를 조절하여 최적의 종목을 다시 분석합니다." 
    />

    <div class="max-w-3xl mx-auto mb-12">
      <BaseCard class="bg-white border border-gray-100 shadow-xl rounded-3xl p-8">
        <h3 class="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
          🎯 투자 전략 설정
        </h3>
        

        <div class="mb-10">
          <label class="block text-sm font-bold text-gray-500 mb-3">투자 스타일 (가중치 자동 적용)</label>
          <div class="grid grid-cols-3 gap-4">
            <label v-for="style in styles" :key="style.value" 
                   class="cursor-pointer border rounded-2xl px-4 py-4 flex flex-col items-center gap-2 transition-all select-none hover:shadow-sm"
                   :class="userProfile.investment_style === style.value 
                     ? 'bg-blue-50 border-blue-500 text-blue-700 ring-1 ring-blue-500 font-bold shadow-md' 
                     : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'"
            >
              <input type="radio" :value="style.value" v-model="userProfile.investment_style" class="hidden">
              <span class="text-3xl">{{ style.icon }}</span>
              <span class="text-base">{{ style.label }}</span>
            </label>
          </div>
        </div>

        <button @click="handleAnalyze" class="btn bg-blue-600 text-white hover:bg-blue-700 w-full border-none shadow-lg text-lg h-14 rounded-2xl">
          선택한 전략으로 종목 다시 분석하기 🔄
        </button>
      </BaseCard>
    </div>

    <BaseCard class="bg-white border border-gray-100 shadow-xl rounded-3xl overflow-hidden">
      <div class="p-6 border-b border-gray-100 flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="flex items-center gap-3">
          <h3 class="text-xl font-bold text-gray-800 flex items-center gap-2">
            📊 맞춤 추천 랭킹
          </h3>
          <span v-if="baseDate" class="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded">
            {{ baseDate }} 기준
          </span>
        </div>
        <button @click="fetchData" class="btn btn-sm btn-ghost gap-2 border border-gray-200 bg-white hover:bg-gray-50">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" /></svg>
          실시간 랭킹 새로고침
        </button>
      </div>

      <div class="overflow-x-auto">
        <table class="table w-full">
          <thead>
            <tr class="bg-gray-50 text-gray-500 text-sm uppercase">
              <th class="py-4 pl-8 text-left">순위</th>
              <th class="py-4 text-left">종목명</th>
              <th class="py-4 text-center">종합점수</th>
              <th class="py-4 text-right">배당률(%)</th>
              <th class="py-4 text-right">ROE(%)</th>
              <th class="py-4 text-right">PER</th>
              <th class="py-4 text-right">PBR</th>
              <th class="py-4 pr-8 text-center">섹터</th>
            </tr>
          </thead>
          
          <tbody>
            <tr v-if="loading">
              <td colspan="8" class="text-center py-20">
                <span class="loading loading-spinner loading-lg text-primary"></span>
              </td>
            </tr>
            <tr v-else-if="stocks.length === 0">
              <td colspan="8" class="text-center py-20 text-gray-400">
                추천할 종목이 없습니다. 투자 성향을 설정하거나 새로고침 해보세요.
              </td>
            </tr>
            <tr v-else v-for="(stock, index) in stocks" :key="stock.ticker" class="hover:bg-blue-50/50 transition-colors border-b border-gray-50 group cursor-pointer">
              <td class="py-4 pl-8 font-bold text-lg text-blue-600">{{ index + 1 }}</td>
              <td class="py-4 font-bold text-gray-800 flex items-center gap-2">
                {{ stock.name }}
                <span class="text-xs font-normal text-gray-400">{{ stock.ticker }}</span>
              </td>
              <td class="py-4 text-center">
                <div class="badge badge-primary badge-outline font-bold">{{ stock.score }}점</div>
              </td>
              <td class="py-4 text-right font-medium text-red-500">{{ stock.DIV }}%</td>
              <td class="py-4 text-right">{{ stock.ROE_est ? stock.ROE_est.toFixed(2) : '-' }}</td>
              <td class="py-4 text-right">{{ stock.PER }}</td>
              <td class="py-4 text-right">{{ stock.PBR }}</td>
              <td class="py-4 pr-8 text-center">
                <span class="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs">{{ stock.Sector }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div class="p-6 bg-gray-50 text-center text-xs text-gray-400 border-t border-gray-100">
        분석 결과는 투자 참고용일 뿐입니다. (제공: FinanceDataReader)
      </div>
    </BaseCard>

  </div>
</template> 