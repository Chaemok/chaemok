import { defineStore } from 'pinia'
import api from '@/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null, // 로그인한 유저의 상세 정보
    isLoading: false, // 로딩 상태 제어
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
  },

  actions: {
    // 🐜 1. 유저 정보 로드 (상세 프로필 포함)
    async getUserInfo() {
      if (!this.token) return
      try {
        const res = await api.get('accounts/user/')
        this.user = res.data
      } catch (err) {
        console.error('유저 정보 로드 실패:', err)
        this.logout()
      }
    },

    // 🐜 2. 로그인 (기존 로직 유지)
    async login(payload) {
      this.isLoading = true
      try {
        const res = await api.post('accounts/login/', payload)
        this.token = res.data.key
        localStorage.setItem('token', this.token)
        await this.getUserInfo()
        router.push({ name: 'home' })
      } catch (err) {
        console.error('로그인 실패:', err)
        alert('아이디 또는 비밀번호를 확인해주세요.')
      } finally {
        this.isLoading = false
      }
    },

    // 🐜 3. 회원가입 (필드명 매핑 로직 추가)
    async signup(payload) {
      this.isLoading = true
      try {
        // [수정 포인트] dj-rest-auth는 password1, password2를 요구해!
        // DB 저장은 장고가 password 하나로 합쳐서 알아서 해줄 거야.
        const signupData = {
          ...payload,
          password1: payload.password,         // 폼의 password를 password1로 매핑
          password2: payload.passwordConfirm   // 폼의 passwordConfirm을 password2로 매핑
        }

        const res = await api.post('accounts/registration/', signupData)
        
        this.token = res.data.key
        localStorage.setItem('token', this.token)
        await this.getUserInfo()
        
        alert('스마트한 개미가 되신 것을 환영합니다! 🐜')
        router.push({ name: 'home' })
      } catch (err) {
        console.error('회원가입 실패:', err)
        // 백엔드 에러 메시지 추출 (예: "이미 사용 중인 이메일입니다.")
        const errorData = err.response?.data
        const errorMsg = errorData ? Object.values(errorData).flat()[0] : '가입 정보를 확인해주세요.'
        alert(errorMsg)
      } finally {
        this.isLoading = false
      }
    },

    // 🐜 4. 중복 확인 (GET 방식)
    async checkUsername(username) {
      try {
        const res = await api.get(`accounts/check-username/${username}/`)
        return res.data 
      } catch (err) {
        console.error('아이디 중복확인 에러:', err)
        return { available: false, message: '서버 에러가 발생했습니다.' }
      }
    },

    async checkNickname(nickname) {
      try {
        const res = await api.get(`accounts/check-nickname/${nickname}/`)
        return res.data
      } catch (err) {
        console.error('닉네임 중복확인 에러:', err)
        return { available: false, message: '서버 에러가 발생했습니다.' }
      }
    },

    // 🐜 5. 로그아웃
    async logout() {
      try {
        // 🐜 서버 세션 종료 시도
        await api.post('accounts/logout/')
      } catch (err) {
        console.warn('서버 로그아웃 요청 실패:', err)
      } finally {
        // 🐜 [수정] 무조건 로컬 정보 지우고 '메인 페이지'로 이동
        this.token = null
        this.user = null
        localStorage.removeItem('token')
        
        // 🐜 로그아웃 알림 (브라우저 기본 alert 대신 토스트가 좋지만 우선은 이렇게!)
        alert('로그아웃되었습니다. 다음에 또 만나요! 🐜')
        
        // 🐜 [핵심] 로그아웃 후 메인 페이지로 이동
        router.push({ name: 'home' })
      }
    },
    async verifyPassword(password) {
      try {
        // 🐜 백엔드에 비밀번호 검증 요청 (커스텀 엔드포인트 필요)
        const res = await api.post('accounts/verify-password/', { password })
        return res.data.success // true/false 반환
      } catch (err) {
        console.error('비밀번호 확인 실패:', err)
        return false
      }
    },
    async updateProfile(formData) {
      try {
        // 🐜 이미지 파일이 포함될 수 있으므로 전송 시 Content-Type 주의
        const res = await api.patch('accounts/user/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        this.user = res.data // 수정된 정보로 즉시 갱신
        return true
      } catch (err) {
        console.error('프로필 수정 실패:', err)
        return false
      }
    }
  }
})  