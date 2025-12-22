// src/api/index.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // 네 API 주소 확인
})

// 🐜 [핵심] 모든 API 요청 전에 실행되는 인터셉터 추가
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    // Django TokenAuthentication은 'Token <key>' 형식을 사용함
    config.headers.Authorization = `Token ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

export default api