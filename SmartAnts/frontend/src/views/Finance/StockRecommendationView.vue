<script setup>
import { ref, onMounted, reactive, computed } from 'vue'
import instance from '@/api/index'
import { useAuthStore } from '@/stores/auth' 
import { useFinanceStore } from '@/stores/finance'
import PageHeader from '@/components/common/PageHeader.vue'

const authStore = useAuthStore()
const financeStore = useFinanceStore()

const loading = ref(true)
const stocks = ref([]) // 전체 목록 (약 200개)
const baseDate = ref('')
const selectedSector = ref('전체') // 현재 선택된 섹터

// 🐜 GICS 11개 섹터 목록
const sectors = [
  '전체', 
  'IT', '커뮤니케이션', '헬스케어', '금융', 
  '경기소비재', '필수소비재', '산업재', '소재', 
  '에너지', '유틸리티', '부동산'
]

// 투자 성향
const userProfile = reactive({
  investment_style: 'balanced'
})

const styles = [
  { label: '안정형', value: 'stable', icon: '🛡️', desc: '배당 중심, 잃지 않는 투자' },
  { label: '균형형', value: 'balanced', icon: '⚖️', desc: '성장과 가치의 조화' },
  { label: '공격형', value: 'aggressive', icon: '🔥', desc: '오직 수익성(ROE) 승부' },
]

// 가중치 설정 (백엔드와 동일)
const weightMap = {
  stable:     { w_div: 0.60, w_roe: 0.10, w_per: 0.15, w_pbr: 0.15 },
  balanced:   { w_div: 0.30, w_roe: 0.30, w_per: 0.20, w_pbr: 0.20 },
  aggressive: { w_div: 0.00, w_roe: 0.70, w_per: 0.15, w_pbr: 0.15 }
}

const fetchData = async () => {
  loading.value = true
  const currentWeights = weightMap[userProfile.investment_style]

  try {
    const res = await instance.get('/finlife/recommend-stocks/', {
      params: currentWeights 
    })
    
    if (res.data.rows) {
      stocks.value = res.data.rows
      baseDate.value = res.data.base_date
      
      // 🐜 [여기!] 콘솔에 전체 데이터를 찍어서 눈으로 확인하기
      console.log("🐜 퀀트 분석 전체 데이터 (200개):", stocks.value)
      
      // 섹터별로 몇 개인지 카운트해서 보여주기 (기타가 얼마나 남았나 확인용)
      const sectorCount = stocks.value.reduce((acc, cur) => {
        acc[cur.Sector] = (acc[cur.Sector] || 0) + 1
        return acc
      }, {})
      console.log("📊 섹터별 종목 수:", sectorCount)

    } else {
      stocks.value = res.data
    }
  } catch (err) {
    console.error("데이터 로딩 실패:", err)
    stocks.value = []
  } finally {
    loading.value = false
  }
}

// 🐜 [핵심] 프론트엔드 필터링 로직
// 200개 중에서 선택된 섹터에 해당하는 것만 골라내고, 상위 20개만 자름
const filteredStocks = computed(() => {
  let list = stocks.value
  
  if (selectedSector.value !== '전체') {
    list = list.filter(s => s.Sector === selectedSector.value)
  }
  
  // 섹터 내에서도 점수 높은 순으로 20개
  return list.slice(0, 20)
})

const handleAnalyze = () => {
  fetchData()
  selectedSector.value = '전체' // 성향 바꾸면 필터 초기화
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 font-pretendard">
    <PageHeader 
        title="Smart Quant Analysis"
        subtitle="재무제표와 시장 데이터를 분석하여, 당신의 성향에 딱 맞는 종목을 발굴합니다."
        bgClass="bg-violet-900" 
    />

    <div class="max-w-7xl mx-auto px-4 pb-20 -mt-8 relative z-20">
      
      <div class="bg-white rounded-[2.5rem] shadow-xl shadow-slate-200/50 p-8 md:p-10 border border-white mb-10">
        
        <h3 class="text-xl font-black text-slate-800 mb-6 flex items-center gap-2">
          🎯 1. 투자 성향을 선택하세요
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <label v-for="style in styles" :key="style.value" class="relative cursor-pointer group">
            <input type="radio" :value="style.value" v-model="userProfile.investment_style" class="hidden peer">
            <div class="h-full border-2 border-slate-100 rounded-[2rem] p-5 flex flex-col items-center text-center transition-all 
                        peer-checked:border-violet-500 peer-checked:bg-violet-50 peer-checked:text-violet-900
                        group-hover:border-violet-200 bg-slate-50/50">
              <span class="text-3xl mb-2 grayscale group-hover:grayscale-0 transition-all">{{ style.icon }}</span>
              <span class="text-base font-black">{{ style.label }}</span>
              <p class="text-[10px] font-medium opacity-60">{{ style.desc }}</p>
            </div>
          </label>
        </div>

        <div class="border-t border-slate-100 my-8"></div>

        <h3 class="text-xl font-black text-slate-800 mb-6 flex items-center gap-2">
          🏭 2. 관심 업종(Sector) 필터
        </h3>
        <div class="flex flex-wrap gap-2.5 mb-8">
          <button 
            v-for="sector in sectors" :key="sector"
            @click="selectedSector = sector"
            class="px-4 py-2.5 rounded-2xl text-sm font-bold transition-all border"
            :class="selectedSector === sector 
              ? 'bg-violet-600 text-white border-violet-600 shadow-lg shadow-violet-200' 
              : 'bg-white text-slate-500 border-slate-200 hover:border-violet-300 hover:text-violet-600'"
          >
            {{ sector }}
          </button>
        </div>

        <button @click="handleAnalyze" 
                class="w-full py-4 bg-slate-900 text-white text-lg font-black rounded-2xl shadow-lg hover:bg-black transition-all active:scale-95 flex items-center justify-center gap-2">
          <span>🚀 AI 분석 다시 실행하기</span>
        </button>
      </div>

      <div class="bg-white rounded-[2.5rem] shadow-xl shadow-slate-200/50 overflow-hidden border border-white">
        <div class="p-8 border-b border-slate-100 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-50/30">
          <div class="flex items-center gap-3">
            <h3 class="text-xl font-black text-slate-800">
              📊 {{ selectedSector }} 추천 TOP 20
            </h3>
            <span v-if="baseDate" class="text-[10px] font-bold text-slate-400 bg-slate-100 px-2 py-1 rounded-md">
              {{ baseDate }} 기준
            </span>
          </div>
          
          <div class="flex items-center gap-2">
             <span class="text-xs font-bold text-violet-600 bg-violet-50 px-3 py-1.5 rounded-full border border-violet-100">
                총 {{ filteredStocks.length }}개 종목 발굴
             </span>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-slate-50 text-slate-500 font-black uppercase text-[10px] tracking-wider">
              <tr>
                <th class="py-4 pl-8 text-left w-16">Rank</th>
                <th class="py-4 text-left">종목명</th>
                <th class="py-4 text-center">점수</th>
                <th class="py-4 text-right">배당률</th>
                <th class="py-4 text-right">ROE</th>
                <th class="py-4 text-right">PER</th>
                <th class="py-4 text-right pr-8">PBR</th>
                <th class="py-4 text-center pr-8">업종</th>
              </tr>
            </thead>
            
            <tbody class="divide-y divide-slate-50">
              <tr v-if="loading">
                <td colspan="8" class="py-32 text-center">
                  <span class="loading loading-spinner loading-lg text-violet-600 mb-4"></span>
                  <p class="text-slate-400 font-bold animate-pulse">데이터를 수집하고 분석 중입니다... 🐜</p>
                </td>
              </tr>

              <tr v-else-if="filteredStocks.length === 0">
                <td colspan="8" class="py-20 text-center text-slate-400 font-bold">
                  선택하신 조건에 맞는 종목이 없습니다.<br>
                  다른 성향이나 섹터를 선택해보세요.
                </td>
              </tr>

              <tr v-else v-for="(stock, index) in filteredStocks" :key="stock.ticker" 
                  class="hover:bg-violet-50/30 transition-colors group cursor-pointer">
                <td class="py-5 pl-8">
                  <span class="text-lg font-black" :class="index < 3 ? 'text-violet-600' : 'text-slate-300'">
                    {{ index + 1 }}
                  </span>
                </td>
                <td class="py-5">
                  <div>
                    <div class="font-black text-slate-800 text-base group-hover:text-violet-700 transition-colors">{{ stock.name }}</div>
                    <div class="text-[10px] font-bold text-slate-400 tracking-widest">{{ stock.ticker }}</div>
                  </div>
                </td>
                <td class="py-5 text-center">
                  <span class="bg-violet-100 text-violet-700 px-3 py-1 rounded-full font-black text-xs">
                    {{ stock.score }}
                  </span>
                </td>
                <td class="py-5 text-right font-bold text-rose-500">{{ stock.DIV }}%</td>
                <td class="py-5 text-right font-bold text-slate-600">{{ stock.ROE_est ? stock.ROE_est.toFixed(2) : '-' }}%</td>
                <td class="py-5 text-right font-medium text-slate-500">{{ stock.PER }}</td>
                <td class="py-5 text-right pr-8 font-medium text-slate-500">{{ stock.PBR }}</td>
                <td class="py-5 text-center pr-8">
                   <span class="text-[10px] font-bold px-2 py-1 rounded border"
                     :class="stock.Sector === '기타' ? 'text-slate-400 border-slate-200' : 'text-violet-600 border-violet-200 bg-violet-50'">
                     {{ stock.Sector }}
                   </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.font-pretendard { font-family: 'Pretendard', sans-serif; }
</style>
// const weightMap = {
//   stable:     { w_div: 0.60, w_roe: 0.20, w_per: 0.10, w_pbr: 0.10 },
//   balanced:   { w_div: 0.30, w_roe: 0.40, w_per: 0.15, w_pbr: 0.15 },
//   aggressive: { w_div: 0.00, w_roe: 0.50, w_per: 0.30, w_pbr: 0.20 }
// }

