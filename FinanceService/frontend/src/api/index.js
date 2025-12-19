import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // 장고 서버 주소
})

// [중요] 요청 보낼 때마다 토큰이 있으면 헤더에 자동으로 실어주는 인터셉터
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export default api