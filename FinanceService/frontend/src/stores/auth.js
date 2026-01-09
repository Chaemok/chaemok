import { defineStore } from 'pinia'
import api from '@/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null, 
    isLoading: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isLoggedIn: (state) => !!state.token,
    nickname: (state) => state.user?.nickname || state.user?.username || '회원',
  },

  actions: {
    // 🚨 앱 초기화 시 호출
    async initialize() {
      if (this.token) {
        api.defaults.headers.common['Authorization'] = `Token ${this.token}`
        await this.getProfile() // 함수명 변경 반영
      }
    },

    // 🚨 [중요] 외부(finance.js, MyPageView)에서 호출하는 이름으로 통일
    async getProfile() {
      if (!this.token) return
      try {
        const res = await api.get('accounts/user/')
        this.user = res.data
        return res.data // 데이터를 반환해줘야 호출부에서 사용 가능
      } catch (err) {
        console.error('유저 정보 로드 실패:', err)
        if (err.response?.status === 401) {
          this.logout()
        }
        throw err
      }
    },

    // 로그인
    async login(payload) {
      this.isLoading = true
      try {
        const res = await api.post('accounts/login/', payload)
        this.token = res.data.key
        localStorage.setItem('token', this.token)
        api.defaults.headers.common['Authorization'] = `Token ${this.token}`
        
        await this.getProfile()
        router.push({ name: 'home' })
      } catch (err) {
        alert('아이디 또는 비밀번호를 확인해주세요.')
        throw err
      } finally {
        this.isLoading = false
      }
    },

    // 회원가입
    async signup(payload) {
      this.isLoading = true
      try {
        const signupData = {
          username: payload.username,
          password1: payload.password,
          password2: payload.passwordConfirm,
          email: payload.email,
          nickname: payload.nickname
        }
        const res = await api.post('accounts/registration/', signupData)
        this.token = res.data.key
        localStorage.setItem('token', this.token)
        api.defaults.headers.common['Authorization'] = `Token ${this.token}`
        
        await this.getProfile()
        return true 
      } catch (err) {
        const errorDetail = err.response?.data 
        alert(`가입 실패: ${JSON.stringify(errorDetail)}`)
        throw err
      } finally {
        this.isLoading = false
      }
    },

    // 로그아웃
    async logout() {
      try { await api.post('accounts/logout/') } catch (e) {}
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
      router.push({ name: 'home' })
    },

    // 비밀번호 확인
    async verifyPassword(passwordInput) {
      try {
        const username = this.user?.username
        if (!username) return false
        await api.post('accounts/login/', { username, password: passwordInput })
        return true
      } catch { return false }
    }
  }
})