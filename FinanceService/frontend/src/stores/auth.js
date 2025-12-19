// frontend/src/stores/auth.js
import { defineStore } from 'pinia'
import api from '@/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    // 🐜 로그인 액션
    async login(payload) {
      try {
        const res = await api.post('accounts/login/', payload)
        this.token = res.data.key
        localStorage.setItem('token', this.token)
        // 로그인 성공 후 홈으로 이동
        router.push({ name: 'home' })
      } catch (err) {
        console.error('로그인 실패:', err)
        alert('아이디 또는 비밀번호를 확인해주세요.')
      }
    },
    // 🐜 로그아웃 액션
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      router.push({ name: 'login' })
    }
  }
})