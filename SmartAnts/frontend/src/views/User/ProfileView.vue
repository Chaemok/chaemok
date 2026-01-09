<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import SecurityModal from '@/components/auth/SecurityModal.vue'

const authStore = useAuthStore()
const router = useRouter()
const isVerified = ref(false)
const showModal = ref(true)

const handleVerify = async (password) => {
  const isValid = await authStore.verifyPassword(password)
  
  if (isValid) {
    isVerified.value = true
    showModal.value = false 
  } else {
    alert('비밀번호가 일치하지 않습니다. 다시 시도해주세요. 🐜')
  }
}

// 🐜 직업 코드 한글 변환
const jobLabel = computed(() => {
  const jobMap = {
    'student': '학생', 'employee': '직장인', 'civil_servant': '공무원',
    'professional': '전문직', 'freelancer': '프리랜서', 
    'business': '사업자', 'housewife': '주부', 'unemployed': '무직', 'etc': '기타'
  }
  return jobMap[authStore.user?.job] || '미지정'
})

// 🐜 투자 성향 텍스트 변환
const riskLabel = computed(() => {
  const levels = {
    1: '안정형 🐢', 2: '안정추구형 🐇', 3: '위험중립형 🦊', 
    4: '적극투자형 🐯', 5: '공격투자형 🦅'
  }
  return levels[authStore.user?.risk_appetite] || '미지정'
})

// 🐜 금액 포맷팅 (0원, null 처리 포함)
const formatMoney = (val) => {
  if (!val) return '0원'
  return Number(val).toLocaleString() + '원'
}
</script>

<template>
  <div class="max-w-2xl mx-auto py-12 px-4">
    <SecurityModal 
      :isOpen="showModal" 
      @close="router.push({ name: 'mypage' })" 
      @confirm="handleVerify" 
    />

    <div v-if="isVerified" class="animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-2xl font-black text-slate-900">상세 회원정보 🔒</h1>
        <router-link :to="{ name: 'mypage' }" class="text-sm font-bold text-slate-400 hover:text-slate-600">
          마이페이지로 돌아가기
        </router-link>
      </div>
      
      <div class="bg-white rounded-[2.5rem] border border-slate-100 shadow-xl p-8 space-y-8">
        
        <div class="space-y-6">
          <h3 class="text-sm font-bold text-slate-400 border-b border-slate-100 pb-2">기본 정보</h3>
          <div v-for="(val, label) in {
            '아이디': authStore.user?.username,
            '이메일': authStore.user?.email,
            '실명': authStore.user?.name || '미등록',
            '닉네임': authStore.user?.nickname || '미등록',
            '연락처': authStore.user?.phone_number || '미등록',
            '생년월일': authStore.user?.birth_date || '미등록',
          }" :key="label" class="flex justify-between items-center">
            <span class="text-xs font-black text-slate-500">{{ label }}</span>
            <span class="font-bold text-slate-800">{{ val }}</span>
          </div>
        </div>

        <div class="space-y-6">
          <h3 class="text-sm font-bold text-slate-400 border-b border-slate-100 pb-2">금융 프로필</h3>
          
          <div class="flex justify-between items-center">
            <span class="text-xs font-black text-slate-500">직업</span>
            <span class="font-bold text-slate-800">{{ jobLabel }}</span>
          </div>

          <div class="flex justify-between items-center">
            <span class="text-xs font-black text-slate-500">운용 자산</span>
            <span class="font-bold text-blue-600">{{ formatMoney(authStore.user?.money) }}</span>
          </div>

          <div class="flex justify-between items-center">
            <span class="text-xs font-black text-slate-500">연봉</span>
            <span class="font-bold text-slate-800">{{ formatMoney(authStore.user?.salary) }}</span>
          </div>

          <div class="flex justify-between items-center">
            <span class="text-xs font-black text-slate-500">투자 성향</span>
            <span class="font-bold text-slate-800 bg-slate-100 px-2 py-1 rounded text-sm">
              {{ riskLabel }}
            </span>
          </div>
          
          <div class="flex justify-between items-center pt-4 text-xs text-slate-400">
            <span>가입일</span>
            <span>{{ authStore.user?.date_joined?.slice(0, 10) }}</span>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>