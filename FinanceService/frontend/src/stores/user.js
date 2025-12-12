// frontend/src/stores/user.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useUserStore = defineStore('user', () => {
  const router = useRouter()
  
  // 1. State: localStorage에서 토큰이 있으면 꺼내서 초기화 (새로고침 해도 유지됨!)
  const token = ref(localStorage.getItem('token'))
  const username = ref(localStorage.getItem('username')) 
  
  const nickname = ref(null)
  const email = ref(null)
  const name = ref(null) 
  const profileImage = ref(null) 

  // 2. Getters
  const isLogin = computed(() => token.value !== null)
  const API_URL = 'http://127.0.0.1:8000'

  // 3. Actions
  
  // 닉네임 중복 확인
  const checkNickname = function (nickname) {
    return axios({
      method: 'get',
      url: `${API_URL}/api/accounts/check-nickname/${nickname}/`
    })
  }

  // 아이디 중복 확인
  const checkUsername = function (username) {
    return axios({
      method: 'get',
      url: `${API_URL}/api/accounts/check-username/${username}/`
    })
  }

  // [회원가입]
  const signUp = function (payload) {
    axios({
      method: 'post',
      url: `${API_URL}/api/accounts/signup/`,
      data: payload,
      headers: { 'Content-Type': 'multipart/form-data' }
    })
      .then((res) => {
        alert('회원가입 완료! 자동 로그인합니다.')
        // payload가 FormData일 경우 값을 꺼내는 방식
        const loginUsername = payload.get('username')
        const loginPassword = payload.get('password')
        
        logIn({ username: loginUsername, password: loginPassword }) 
      })
      .catch((err) => {
        console.error(err)
        alert('회원가입 실패: 정보를 확인해주세요.')
      })
  }

  // [로그인]
  const logIn = function (payload) {
    axios({
      method: 'post',
      url: `${API_URL}/api/auth/token/`, // dj-rest-auth나 simplejwt 주소 확인 필요
      data: payload
    })
      .then((res) => {
        // 응답으로 받은 토큰 저장
        const newToken = res.data.access || res.data.key
        token.value = newToken
        username.value = payload.username

        // [중요] 새로고침 해도 로그인 유지되도록 로컬스토리지에 저장
        localStorage.setItem('token', newToken)
        localStorage.setItem('username', payload.username)

        // 내 정보 갱신
        getMe()
        
        alert('로그인 성공!')
        router.push({ name: 'home' })
      })
      .catch((err) => {
        console.error(err)
        alert('로그인 실패: 아이디와 비밀번호를 확인하세요.')
      })
  }

  // [내 정보 가져오기]
  const getMe = function () {
    if (!token.value) return

    axios({
      method: 'get',
      url: `${API_URL}/api/accounts/me/`, // 백엔드 URL 확인 필요 (보통 /user/ 또는 /me/)
      headers: { Authorization: `Bearer ${token.value}` }
    })
    .then((res) => {
      // 받아온 정보 저장
      nickname.value = res.data.nickname
      email.value = res.data.email
      name.value = res.data.name
      // 프로필 이미지가 있다면 저장
      if (res.data.profile_image) {
        profileImage.value = res.data.profile_image
      }
    })
    .catch((err) => {
      console.error('내 정보 로드 실패:', err)
      // 토큰이 만료되었을 경우 로그아웃 처리 등을 할 수 있음
      if (err.response && err.response.status === 401) {
        logOut()
      }
    })
  }

  // [회원 정보 수정]
  const updateProfile = function (payload) {
    axios({
      method: 'put',
      url: `${API_URL}/api/accounts/me/`,
      data: payload,
      headers: { 
        Authorization: `Bearer ${token.value}`,
        'Content-Type': 'multipart/form-data' 
      }
    })
      .then((res) => {
        alert('회원 정보 수정 완료!')
        nickname.value = res.data.nickname
        email.value = res.data.email
        if (res.data.profile_image) profileImage.value = res.data.profile_image
        router.push({ name: 'profile' })
      })
      .catch((err) => {
        console.error(err)
        alert('수정 실패')
      })
  }

  // [로그아웃]
  const logOut = function () {
    token.value = null
    username.value = null
    nickname.value = null
    email.value = null
    name.value = null
    profileImage.value = null
    
    // [중요] 로컬스토리지에서도 삭제
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    
    alert('로그아웃 되었습니다.')
    router.push({ name: 'home' })
  }

  return { 
    token, username, nickname, email, name, profileImage, isLogin, API_URL,
    signUp, logIn, getMe, updateProfile, logOut, checkUsername, checkNickname
  }
})