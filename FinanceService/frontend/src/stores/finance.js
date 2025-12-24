import { defineStore } from 'pinia'
import api from '@/api' // axios 인스턴스 (설정된 파일 경로 확인 필요)

export const useFinanceStore = defineStore('finance', {
  state: () => ({
    // 1. 기존 금융 상품 데이터
    depositProducts: [],
    savingProducts: [],
    exchangeRates: [],
    news: [],
    
    // 2. 🐜 [수정] 실시간 시장 지표 (yfinance 10대 지표 전용)
    // 초기값을 빈 객체 {}로 설정해서 백엔드의 10개 데이터를 통째로 받음
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
    // 특정 통화의 환율 정보를 가져오는 Getter
    getExchangeRate: (state) => (unit) => {
      if (!state.exchangeRates || state.exchangeRates.length === 0) return { deal_bas_r: '0' }
      // USD, EUR 등 통화코드로 검색
      return state.exchangeRates.find(r => r.cur_unit === unit) || { deal_bas_r: '0' }
    }
  },

  actions: {
    /**
     * 💱 환율 정보 가져오기 (ExchangeView.vue를 위해 필수!)
     */
    async getExchangeRates() {
      try {
        const res = await api.get('finlife/exchange-rate/')
        this.exchangeRates = res.data
        console.log('✅ 환율 정보 로드 완료')
      } catch (err) {
        console.error('Exchange Rates 로드 실패:', err)
      }
    },

    /**
     * 🐜 [수정] 실시간 글로벌 시장 지표 가져오기 (yfinance)
     */
    async fetchMarketStatus() {
      this.isMarketLoading = true
      try {
        const res = await api.get('finlife/market-status/')
        // 백엔드에서 온 { "NASDAQ": {...}, "KOSPI": {...} } 구조를 그대로 저장
        this.marketData = res.data 
        console.log('✅ 글로벌 10대 지표 로드 완료 (yfinance)')
      } catch (err) {
        console.error('Market Status 로드 실패:', err)
      } finally {
        this.isMarketLoading = false
      }
    },

    /**
     * 퀀트 엔진 기반 주식 추천 가져오기
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
     * HomeView 진입 시 필요한 데이터 병렬 호출
     * (getExchangeRates를 재사용하여 코드 중복 제거)
     */
    async fetchQuickData() {
      this.isMainLoading = true
      try {
        // 🐜 10대 지표, 추천주, 뉴스, 환율을 병렬로 요청
        await Promise.all([
          this.fetchMarketStatus(),
          this.fetchStockRecommendations(),
          this.getExchangeRates(), // 위에서 만든 함수 재사용
          api.get('finlife/news/').then(res => this.news = res.data)
        ])
        console.log('✅ 메인 화면 모든 데이터 동기화 완료 🐜')
      } catch (err) {
        console.error('Quick Data 로드 실패:', err)
      } finally {
        this.isMainLoading = false
      }
    },

    // 예적금 상품 정보 가져오기
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