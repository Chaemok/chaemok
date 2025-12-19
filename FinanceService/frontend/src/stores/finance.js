import { defineStore } from 'pinia'
import api from '@/api'

export const useFinanceStore = defineStore('finance', {
  state: () => ({
    depositProducts: [],
    savingProducts: [],
    exchangeRates: [],
    news: [],
    topStocks: [],
    isMainLoading: false,
    isStockLoading: false,
  }),

  getters: {
    // 🐜 [필수] HomeView에서 환율을 부를 때 쓰는 함수형 게터
    getExchangeRate: (state) => (unit) => {
      if (!state.exchangeRates || state.exchangeRates.length === 0) return { deal_bas_r: '0' }
      return state.exchangeRates.find(r => r.cur_unit === unit) || { deal_bas_r: '0' }
    }
  },

  actions: {
    // 🐜 [필수] HomeView 19번 라인에서 에러 나는 바로 그 함수!
    async fetchQuickData() {
      this.isMainLoading = true
      try {
        const [newsRes, exchangeRes] = await Promise.all([
          api.get('finlife/news/'),
          api.get('finlife/exchange-rate/')
        ])
        this.news = newsRes.data
        this.exchangeRates = exchangeRes.data
        console.log('✅ 퀵 데이터 로드 완료')
      } catch (err) {
        console.error('Quick Data 로드 실패:', err)
      } finally {
        this.isMainLoading = false
      }
    },

    // 🐜 예적금 리스트용 함수들
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
    },

    // 주식 랭킹용
    async fetchStockRanking() {
      this.isStockLoading = true
      try {
        const res = await api.get('finlife/stocks/top/')
        this.topStocks = res.data.rows
      } catch (err) { console.error(err) } finally {
        this.isStockLoading = false
      }
    }
  }
})