<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const props = defineProps({
  isOpen: Boolean,
  product: Object,
  type: { 
    type: String,
    default: 'deposit' 
  }
})

const emit = defineEmits(['close'])
const authStore = useAuthStore()

// 🐜 1. 금리 정보 가공 (기존 코드 유지)
const uniqueOptions = computed(() => {
  if (!props.product) return []

  if (props.product.options && props.product.options.length > 0) {
    const uniqueMap = new Map()
    props.product.options.forEach(opt => {
      const key = `${opt.save_trm}-${opt.intr_rate}-${opt.intr_rate2}`
      if (!uniqueMap.has(key)) uniqueMap.set(key, opt)
    })
    return Array.from(uniqueMap.values()).sort((a, b) => Number(a.save_trm) - Number(b.save_trm))
  }

  if (props.product.intr_rate !== undefined || props.product.intr_rate2 !== undefined) {
    return [{
      id: props.product.option_id || props.product.id, 
      save_trm: props.product.save_trm || '자율',
      intr_rate: props.product.intr_rate || 0,
      intr_rate2: props.product.intr_rate2 || 0
    }]
  }

  return []
})

// 🐜 2. 가입 신청 함수 (수정됨)
const joinProduct = async (option) => {
  if (!authStore.isLoggedIn) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }
  
  if (!option.id) {
    alert('상품 옵션 정보를 불러올 수 없어 가입을 진행할 수 없습니다.')
    return
  }

  const confirmMsg = `${props.product.fin_prdt_nm} (${option.save_trm}개월)\n상품에 가입하시겠습니까?`
  if (!confirm(confirmMsg)) return

  try {
    // 🐜 [수정 시작] URL 타입 결정 로직 강화 (방어 코드)
    // 기존 코드: const urlType = props.type === 'saving' ? 'savings' : 'deposits'
    
    // 수정 코드: props.type이 'saving'이거나, 상품명에 '적금'이 포함되어 있으면 적금 URL 사용
    let urlType = 'deposits' // 기본값 예금
    
    if (props.type === 'saving' || (props.product.fin_prdt_nm && props.product.fin_prdt_nm.includes('적금'))) {
        urlType = 'savings'
    }
    // 🐜 [수정 끝]

    // 🐜 [확인용 로그] (배포 시 주석 처리 가능)
    // console.log(`가입 요청: /api/finlife/${urlType}/join/${option.id}/`)

    await axios.post(`http://127.0.0.1:8000/api/finlife/${urlType}/join/${option.id}/`, {}, {
      headers: { Authorization: `Token ${authStore.token}` }
    })
    
    // 🐜 가입 성공 메시지 수정
    alert(`🎉 [${option.save_trm}개월] 상품 가입이 완료되었습니다!\n마이페이지에서 확인해보세요.`)
    emit('close')
    
  } catch (err) {
    console.error(err)
    if (err.response?.status === 400) {
      // 🐜 이미 가입된 경우 해지할지 물어보는 로직으로 확장 가능하나, 현재는 알림만
      alert('이미 가입한 상품이거나, 처리할 수 없는 요청입니다.')
    } else {
      alert('가입 처리 중 오류가 발생했습니다.')
    }
  }
}

// 🐜 3. 링크 연결 로직 (기존 유지)
const openProductLink = () => {
  if (!props.product) return
  if (props.product.join_url) { window.open(props.product.join_url, '_blank'); return }
  if (props.product.homp_url) { window.open(props.product.homp_url, '_blank'); return }
  const query = `${props.product.kor_co_nm} ${props.product.fin_prdt_nm}`
  window.open(`https://search.naver.com/search.naver?where=nexearch&query=${encodeURIComponent(query)}`, '_blank')
}
</script>

<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="emit('close')">
      <div class="bg-white w-full max-w-2xl rounded-[3rem] overflow-hidden shadow-2xl animate-modal-up flex flex-col max-h-[90vh]">
        
        <div class="p-8 bg-blue-600 text-white relative shrink-0">
          <button @click="emit('close')" 
                  class="absolute top-6 right-6 text-white/70 hover:text-white transition-colors bg-white/10 hover:bg-white/20 rounded-full w-11 h-11 flex items-center justify-center text-lg shadow-sm backdrop-blur-sm z-10"
                  aria-label="닫기">
            ✕
          </button>
          
          <p class="text-xs font-bold opacity-80 mb-2 tracking-widest uppercase">{{ product?.kor_co_nm }}</p>
          <h2 class="text-3xl font-black leading-tight">{{ product?.fin_prdt_nm }}</h2>
        </div>

        <div class="p-10 space-y-8 overflow-y-auto custom-scrollbar flex-1 bg-slate-50/50">
          
          <div class="grid grid-cols-2 gap-8">
            <div class="bg-white p-5 rounded-3xl border border-slate-100 shadow-sm">
              <h4 class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">가입 대상</h4>
              <p class="font-bold text-slate-800 leading-snug text-sm">{{ product?.join_member || '제한 없음' }}</p>
            </div>
            <div class="bg-white p-5 rounded-3xl border border-slate-100 shadow-sm">
              <h4 class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">가입 방법</h4>
              <p class="font-bold text-slate-800 leading-snug text-sm">{{ product?.join_way || '영업점, 스마트폰' }}</p>
            </div>
          </div>

          <div v-if="uniqueOptions.length">
            <h4 class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-4 ml-1">저축 기간별 금리 & 가입</h4>
            <div class="bg-white border border-slate-100 rounded-2xl overflow-hidden shadow-sm">
              <table class="w-full text-sm">
                <thead class="bg-slate-50 border-b border-slate-100 text-slate-400 font-black text-[10px] uppercase">
                  <tr>
                    <th class="py-4 px-5 text-left">기간</th>
                    <th class="py-4 px-5 text-center">기본</th>
                    <th class="py-4 px-5 text-center text-blue-600">최고</th>
                    <th class="py-4 px-5 text-center">신청</th> </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                  <tr v-for="opt in uniqueOptions" :key="opt.id || opt.save_trm" class="hover:bg-blue-50/50 transition-colors group">
                    <td class="py-4 px-5 font-bold text-slate-600">
                      {{ opt.save_trm === '자율' ? '자율' : `${opt.save_trm}개월` }}
                    </td>
                    <td class="py-4 px-5 text-center font-bold text-slate-800">{{ opt.intr_rate }}%</td>
                    <td class="py-4 px-5 text-center font-black text-blue-600">{{ opt.intr_rate2 }}%</td>
                    <td class="py-3 px-5 text-center">
                      <button 
                        @click="joinProduct(opt)"
                        class="bg-blue-100 text-blue-700 text-[11px] font-bold py-2 px-4 rounded-xl hover:bg-blue-600 hover:text-white transition-all shadow-sm active:scale-95"
                      >
                        가입
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <div v-else class="text-center py-10 bg-white rounded-3xl border border-slate-100">
             <p class="text-slate-400 font-bold text-sm">😢 상세 금리 정보를 불러올 수 없습니다.</p>
          </div>

          <div v-if="product?.etc_note" class="bg-blue-50/50 p-6 rounded-3xl border border-blue-100">
            <h4 class="text-[10px] font-black text-blue-400 uppercase tracking-widest mb-3">상품 유의사항</h4>
            <p class="text-xs text-slate-600 leading-relaxed whitespace-pre-line">{{ product.etc_note }}</p>
          </div>
        </div>

        <div class="p-6 border-t border-slate-50 flex gap-4 bg-white shrink-0">
          <button @click="emit('close')" class="flex-1 py-4 text-slate-400 font-black hover:bg-slate-50 rounded-2xl transition-all">닫기</button>
          
          <button @click="openProductLink" 
                  class="flex-[2] py-4 bg-blue-600 text-white font-black rounded-2xl shadow-lg shadow-blue-100 hover:bg-blue-700 transition-all hover:-translate-y-1 flex items-center justify-center gap-2">
            <span>공식 사이트 확인</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 opacity-80" viewBox="0 0 20 20" fill="currentColor">
              <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.animate-modal-up { animation: modalUp 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
@keyframes modalUp {
  from { opacity: 0; transform: translateY(40px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>  