import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useFinanceStore = defineStore('finance', () => {
  
  // ✨ [핵심 수정] API_URL을 환경 변수에서 가져오도록 변경
  // 1. import.meta.env를 사용하여 .env 파일의 변수를 읽어옵니다.
  // 2. 환경 변수가 없을 경우 (혹은 로컬 개발 시) 안전하게 기본값('http://127.0.0.1:8000')을 사용합니다.
  const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
  
  // 콘솔에 현재 API_URL이 무엇인지 확인용 (선택 사항)
  console.log(`[FinanceStore] API Base URL set to: ${API_URL}`)

  const depositProducts = ref([]) 
  const savingProducts = ref([])  

  const getDepositProducts = () => {
    // API_URL 변수를 사용하여 요청 주소 구성
    axios.get(`${API_URL}/api/finances/deposits/`)
      .then(res => {
        depositProducts.value = res.data
      })
      .catch(err => console.log(err))
  }

  const getSavingProducts = () => {
    // API_URL 변수를 사용하여 요청 주소 구성
    axios.get(`${API_URL}/api/finances/savings/`)
      .then(res => {
        savingProducts.value = res.data
      })
      .catch(err => console.log(err))
  }

  return { 
    API_URL, 
    depositProducts, 
    savingProducts, 
    getDepositProducts, 
    getSavingProducts 
  }
})