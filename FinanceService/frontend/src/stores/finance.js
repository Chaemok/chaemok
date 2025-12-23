import { defineStore } from 'pinia'
import api from '@/api'

export const useFinanceStore = defineStore('finance', {
  state: () => ({
    // 1. 기존 금융 상품 데이터
    depositProducts: [],
    savingProducts: [],
    exchangeRates: [],
    news: [],
    
    // 2. 🐜 [수정] 실시간 시장 지표 (yfinance 10대 지표 전용)
    // 초기값을 빈 객체 {}로 설정해서 백엔드의 10개 데이터를 통째로 받아야 해.
    marketData: {}, 
    
    // 3. 퀀트 엔진 기반 주식 추천 데이터
    recommendedStocks: [],
    baseDate: '',

    // 로딩 상태들
    isMainLoading: false,
    isMarketLoading: false,
    isRecLoading: false,
  }),

  getters: {
    getExchangeRate: (state) => (unit) => {
      if (!state.exchangeRates || state.exchangeRates.length === 0) return { deal_bas_r: '0' }
      return state.exchangeRates.find(r => r.cur_unit === unit) || { deal_bas_r: '0' }
    }
  },

  actions: {
    /**
     * 🐜 [수정] 실시간 글로벌 시장 지표 가져오기
     * 이제 KIS/Gold가 아닌 yfinance 기반 10대 지표를 가져와.
     */
    async fetchMarketStatus() {
      this.isMarketLoading = true
      try {
        const res = await api.get('finlife/market-status/')
        // 백엔드에서 온 { "NASDAQ": {...}, "KOSPI": {...} } 구조를 그대로 저장.
        this.marketData = res.data 
        console.log('✅ 글로벌 10대 지표 로드 완료 (yfinance)')
      } catch (err) {
        console.error('Market Status 로드 실패:', err)
      } finally {
        this.isMarketLoading = false
      }
    },

    /**
     * 퀀트 엔진 기반 주식 추천 가져오기 (기존 유지)
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
     * HomeView 진입 시 필요한 데이터 병렬 호출 (기존 유지)
     */
    async fetchQuickData() {
      this.isMainLoading = true
      try {
        // 🐜 10대 지표를 포함하여 모든 데이터를 한 번에 가져와서 속도를 높여.
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

    // 예적금 상품 정보 가져오기 (기존 유지)
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