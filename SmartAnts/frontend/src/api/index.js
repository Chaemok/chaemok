import axios from 'axios'

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  }
})

// 🚨 요청 인터셉터 (이게 핵심입니다)
// API 요청 쏠 때마다 로컬스토리지 뒤져서 토큰 있으면 강제로 헤더에 박아버립니다.
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      // Django dj-rest-auth 기본 설정은 'Token'입니다.
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default instance