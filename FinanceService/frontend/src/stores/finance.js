import { defineStore } from 'pinia'
import api from '@/api'

export const useFinanceStore = defineStore('finance', {
  state: () => ({
    // 1. 기존 금융 상품 및 뉴스 데이터
    depositProducts: [],
    savingProducts: [],
    exchangeRates: [],
    news: [],
    
    // 2. 🐜 [추가] 실시간 시장 지표 (KIS 주식 + GoldAPI 금/은)
    marketData: {
      stock: null,
      metal: null
    },
    
    // 3. 🐜 [추가] 퀀트 엔진 기반 주식 추천 데이터
    recommendedStocks: [],
    baseDate: '', // 분석 기준일

    // 로딩 상태들
    isMainLoading: false,
    isMarketLoading: false,
    isRecLoading: false,
  }),

  getters: {
    // 특정 통화의 환율 정보를 찾는 게터
    getExchangeRate: (state) => (unit) => {
      if (!state.exchangeRates || state.exchangeRates.length === 0) return { deal_bas_r: '0' }
      return state.exchangeRates.find(r => r.cur_unit === unit) || { deal_bas_r: '0' }
    }
  },

  actions: {
    /**
     * 🐜 [핵심] 실시간 시장 지표 가져오기 (KIS + GoldAPI)
     * Django의 get_market_status 뷰를 호출합니다.
     */
    async fetchMarketStatus() {
      this.isMarketLoading = true
      try {
        const res = await api.get('finlife/market-status/')
        this.marketData = res.data
        console.log('✅ 실시간 시장 지표 로드 완료 (KIS/Gold)')
      } catch (err) {
        console.error('Market Status 로드 실패:', err)
      } finally {
        this.isMarketLoading = false
      }
    },

    /**
     * 🐜 [핵심] 퀀트 엔진 기반 주식 추천 가져오기
     * 네가 만든 utils.py의 분석 로직 결과를 가져옵니다.
     */
    async fetchStockRecommendations() {
      this.isRecLoading = true
      try {
        const res = await api.get('finlife/recommend-stocks/')
        this.recommendedStocks = res.data.rows
        this.baseDate = res.data.base_date
        console.log('✅ 퀀트 기반 주식 추천 로드 완료')
      } catch (err) {
        console.error('Stock Recommendations 로드 실패:', err)
      } finally {
        this.isRecLoading = false
      }
    },

    /**
     * HomeView 진입 시 필요한 기본 데이터들을 한 번에 호출
     */
    async fetchQuickData() {
      this.isMainLoading = true
      try {
        // 기존 환율/뉴스 + 실시간 지수 + 주식 추천을 병렬로 호출하여 속도 최적화
        await Promise.all([
          this.fetchMarketStatus(),
          this.fetchStockRecommendations(),
          api.get('finlife/news/').then(res => this.news = res.data),
          api.get('finlife/exchange-rate/').then(res => this.exchangeRates = res.data)
        ])
        console.log('✅ 메인 화면 모든 데이터 동기화 완료 🐜')
      } catch (err) {
        console.error('Quick Data 로드 실패:', err)
      } finally {
        this.isMainLoading = false
      }
    },

    // 예적금 상품 정보 가져오기 (필요 시 호출)
    async getDepositProducts() {
      try {
        const res = await api.get('finlife/deposits/')
        this.depositProducts = res.data
      } catch (err) { console.error(err) }
    },

    async getSavingProducts() {
      try {
        const res = await api.get('finlife/savings/')
        this.savingProducts = res.data
      } catch (err) { console.error(err) }
    }
  }
})