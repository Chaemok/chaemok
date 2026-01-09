import { defineStore } from 'pinia'
import api from '@/api' // 👈 위에서 설정한 axios 인스턴스
import { useAuthStore } from '@/stores/auth' // 👈 유저 정보 갱신용

export const useFinanceStore = defineStore('finance', {
  state: () => ({
    // 1. 금융 상품 데이터
    depositProducts: [],
    savingProducts: [],
    exchangeRates: [],
    news: [],
    
    // 2. 실시간 시장 지표
    marketData: {}, 
    
    // 3. 추천 데이터
    recommendedStocks: [],
    baseDate: '',
    depositRecommendations: { type: '', message: '', data: [] },

    // 4. 내가 가입한 상품 목록 (AuthStore와 동기화됨)
    joined: {
      deposits: [],
      savings: [],
    },

    // 로딩 상태
    isMainLoading: false,
    isMarketLoading: false,
    isRecLoading: false,
  }),

  getters: {
    // 특정 통화 환율 가져오기 (안전한 접근)
    getExchangeRate: (state) => (unit) => {
      if (!state.exchangeRates || state.exchangeRates.length === 0) return { deal_bas_r: '0' }
      return state.exchangeRates.find(r => r.cur_unit === unit) || { deal_bas_r: '0' }
    },
    // 가입 여부 확인용 Set (빠른 조회)
    joinedDepositOptionIds: (state) => new Set(state.joined.deposits.map(o => o.id)),
    joinedSavingOptionIds: (state) => new Set(state.joined.savings.map(o => o.id)),
  },

  actions: {
    /**
     * 💱 환율 정보 가져오기
     */
    async getExchangeRates() {
      try {
        const res = await api.get('finlife/exchange-rate/')
        this.exchangeRates = res.data
      } catch (err) {
        console.error('Exchange Rates 로드 실패:', err)
      }
    },

    /**
     * 📈 글로벌 시장 지표 (yfinance)
     */
    async fetchMarketStatus() {
      this.isMarketLoading = true
      try {
        const res = await api.get('finlife/market-status/')
        this.marketData = res.data 
      } catch (err) {
        console.error('Market Status 로드 실패:', err)
      } finally {
        this.isMarketLoading = false
      }
    },

    /**
     * 📊 퀀트 주식 추천
     */
    async fetchStockRecommendations() {
      this.isRecLoading = true
      try {
        const res = await api.get('finlife/recommend-stocks/')
        this.recommendedStocks = res.data.rows
        this.baseDate = res.data.base_date
      } catch (err) {
        console.error('Stock Recommendations 로드 실패:', err)
      } finally {
        this.isRecLoading = false
      }
    },

    /**
     * 📰 뉴스 검색
     */
    async fetchNews(payload = {}) {
      this.isMainLoading = true
      try {
        const { query, category } = payload
        const res = await api.get('finlife/news/', { params: { query, category } })
        this.news = res.data
      } catch (err) {
        console.error('뉴스 로드 실패:', err)
      } finally {
        this.isMainLoading = false
      }
    },
    /**
     * 💰 예금 상품 목록 가져오기
     */
    async getDepositProducts() {
      try {
        const res = await api.get('finlife/deposits/') // urls.py의 'deposits/'와 매칭
        this.depositProducts = res.data
      } catch (err) {
        console.error('예금 로드 실패:', err)
        throw err
      }
    },

    /**
     * 🐖 적금 상품 목록 가져오기
     */
    async getSavingProducts() {
      try {
        const res = await api.get('finlife/savings/') // urls.py의 'savings/'와 매칭
        this.savingProducts = res.data
      } catch (err) {
        console.error('적금 로드 실패:', err)
        throw err
      }
    },

    /**
     * 🎁 맞춤 상품 추천 (알고리즘)
     */
    async fetchRecommendations() {
      // 로그인 안했으면 패스
      const authStore = useAuthStore()
      if (!authStore.token) return

      this.isRecLoading = true
      try {
        const res = await api.get('finlife/recommend/') // URL 확인 (recommend vs recommend-algo)
        this.depositRecommendations = res.data 
      } catch (err) {
        console.error('추천 상품 로드 실패:', err)
      } finally {
        this.isRecLoading = false
      }
    },

    /**
     * 🔒 가입한 상품 목록 동기화
     * (AuthStore의 최신 정보를 가져와서 FinanceStore 상태도 업데이트)
     */
    async fetchJoinedProducts() {
      const authStore = useAuthStore()
      // 1. 유저 정보 갱신 요청
      await authStore.getProfile()
      
      // 2. 갱신된 유저 정보에서 가입 목록 가져오기
      if (authStore.user) {
        this.joined.deposits = authStore.user.joined_deposits || []
        this.joined.savings = authStore.user.joined_savings || []
      }
    },

    /**
     * ✅ 예금 가입/해지 토글
     */
    async toggleDepositJoin(optionId) {
      try {
        // 백엔드: path('deposits/join/<int:option_pk>/', ...)
        // 🚨 주소 순서를 백엔드와 맞췄습니다.
        await api.post(`finlife/deposits/join/${optionId}/`)
        
        await this.fetchJoinedProducts() 
        await this.fetchRecommendations()
      } catch (err) {
        console.error('예금 가입 토글 실패:', err)
        throw err
      }
    },

    /**
     * ✅ 적금 가입/해지 토글
     */
    async toggleSavingJoin(optionId) {
      try {
        // 백엔드: path('savings/join/<int:option_pk>/', ...)
        await api.post(`finlife/savings/join/${optionId}/`)
        
        await this.fetchJoinedProducts()
        await this.fetchRecommendations()
      } catch (err) {
        console.error('적금 가입 토글 실패:', err)
        throw err
      }
    },
    
    /**
     * 🚀 메인 데이터 병렬 로드 (HomeView 진입 시)
     */
    async fetchQuickData() {
      this.isMainLoading = true
      try {
        await Promise.all([
          this.fetchMarketStatus(),
          this.fetchStockRecommendations(),
          this.getExchangeRates(),
          this.fetchNews()
        ])
        
        // 로그인 상태라면 추천 목록도 갱신
        const authStore = useAuthStore()
        if (authStore.token) {
          await this.fetchJoinedProducts() // 가입 목록 갱신
          await this.fetchRecommendations() // 추천 목록 갱신
        }
        
      } catch (err) {
        console.error('Quick Data 로드 실패:', err)
      } finally {
        this.isMainLoading = false
      }
    }
  }
})