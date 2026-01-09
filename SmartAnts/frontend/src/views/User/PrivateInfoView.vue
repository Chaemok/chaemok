<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import SecurityModal from '@/components/auth/SecurityModal.vue' // 방금 만든 모달 가져오기

const authStore = useAuthStore()
const router = useRouter()

const isVerified = ref(false) // 인증 완료 여부
const showModal = ref(true)   // 모달 표시 여부

// 모달에서 '확인' 눌렀을 때 실행
const handleVerify = async (passwordInput) => {
  // 스토어의 verifyPassword 함수 호출 (로그인 시도로 검증)
  const success = await authStore.verifyPassword(passwordInput)
  
  if (success) {
    isVerified.value = true // 인증 성공 -> 정보 보여줌
    showModal.value = false // 모달 닫기
  } else {
    alert('비밀번호가 일치하지 않습니다. 다시 시도해주세요. 🐜')
  }
}

// 모달 '취소' 눌렀을 때
const handleClose = () => {
  router.push({ name: 'mypage' }) // 마이페이지로 돌아감
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 py-12 px-4">
    
    <SecurityModal 
      :isOpen="showModal" 
      @close="handleClose" 
      @confirm="handleVerify" 
    />

    <div v-if="isVerified" class="max-w-2xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
      
      <div class="flex items-center justify-between mb-8 px-2">
        <h1 class="text-2xl font-black text-slate-900">상세 회원정보 🔒</h1>
        <button @click="router.push({ name: 'mypage' })" class="text-sm font-bold text-slate-400 hover:text-slate-600">
          마이페이지로 돌아가기
        </button>
      </div>
      
      <div class="bg-white rounded-[2.5rem] border border-slate-100 shadow-xl p-8 md:p-10 space-y-8">
        
        <div class="flex items-center gap-6 pb-8 border-b border-slate-50">
          <div class="w-20 h-20 rounded-full bg-slate-100 overflow-hidden border border-slate-200">
             <img v-if="authStore.user?.profile_image" :src="'http://127.0.0.1:8000' + authStore.user.profile_image" class="w-full h-full object-cover" />
             <div v-else class="w-full h-full flex items-center justify-center text-3xl">🐜</div>
          </div>
          <div>
            <h2 class="text-xl font-black text-slate-900">{{ authStore.user?.nickname }}</h2>
            <p class="text-sm text-slate-400 font-bold">@{{ authStore.user?.username }}</p>
          </div>
        </div>

        <div class="space-y-6">
          <div v-for="(val, label) in {
            '아이디': authStore.user?.username,
            '이메일': authStore.user?.email,
            '연락처': authStore.user?.phone_number || '미등록',
            '생년월일': authStore.user?.birth_date || '미등록',
            '가입일': authStore.user?.date_joined?.slice(0, 10),
            '자산 규모': (authStore.user?.money?.toLocaleString() || 0) + '원',
            '연봉': (authStore.user?.salary?.toLocaleString() || 0) + '원'
          }" :key="label" class="flex justify-between items-center border-b border-slate-50 pb-4 last:border-0 last:pb-0">
            <span class="text-xs font-black text-slate-400 uppercase tracking-widest">{{ label }}</span>
            <span class="font-bold text-slate-800">{{ val }}</span>
          </div>
        </div>

        <div class="pt-4">
          <router-link :to="{ name: 'profile-edit' }" 
            class="flex w-full h-14 items-center justify-center rounded-2xl bg-slate-900 text-white font-bold hover:bg-blue-600 shadow-lg shadow-blue-100 transition-all">
            정보 수정하러 가기 ✏️
          </router-link>
        </div>

      </div>
    </div>

  </div>
</template>