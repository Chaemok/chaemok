<script setup>
import { reactive, ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const emit = defineEmits(['submit'])

const isIdAvailable = ref(false)
const isNicknameAvailable = ref(false)

const form = reactive({
  username: '', 
  password: '', 
  passwordConfirm: '',
  email: '', 
  name: '', 
  nickname: '', 
  phone_number: '', 
  birth_date: null,
  // 🐜 백엔드 시리얼라이저 요구사항에 맞춘 기본값 추가
  money: 0,
  salary: 0,
  job: 'etc',
  risk_appetite: 3
})

// 🐜 실시간 비밀번호 확인
const isPasswordMatch = computed(() => {
  return form.password && form.passwordConfirm && form.password === form.passwordConfirm
})

// 🐜 ID 중복 확인 수정
const checkId = async () => {
  if (!form.username) return alert('아이디를 입력해주세요.')
  
  // 스토어에서 boolean 값을 직접 받아옵니다.
  const available = await authStore.checkUsername(form.username)
  isIdAvailable.value = available
  
  if (available) {
    alert('사용 가능한 아이디입니다. ✅')
  } else {
    alert('이미 사용 중인 아이디입니다. ❌')
  }
}

// 🐜 닉네임 중복 확인 수정
const checkNickname = async () => {
  if (!form.nickname) return alert('닉네임을 입력해주세요.')
  
  const available = await authStore.checkNickname(form.nickname)
  isNicknameAvailable.value = available
  
  if (available) {
    alert('사용 가능한 닉네임입니다. ✅')
  } else {
    alert('이미 사용 중인 닉네임입니다. ❌')
  }
}

const onSubmit = () => {
  if (!isIdAvailable.value) return alert('아이디 중복 확인이 필요합니다.')
  if (!isNicknameAvailable.value) return alert('닉네임 중복 확인이 필요합니다.')
  if (!form.password || !form.passwordConfirm) return alert('비밀번호를 입력해주세요.')
  if (!isPasswordMatch.value) return alert('비밀번호가 일치하지 않습니다.')
  if (!form.email) return alert('이메일을 입력해주세요.')
  
  // 폼 데이터를 부모 컴포넌트(SignupView)로 전달
  emit('submit', { ...form })
}
</script>

<template>
  <form @submit.prevent="onSubmit" class="space-y-5">
    <div class="space-y-1 animate-stagger-1">
      <div class="flex gap-2">
        <input 
          v-model="form.username" 
          type="text" 
          placeholder="아이디" 
          @input="isIdAvailable = false"
          class="flex-1 h-11 px-4 rounded-xl bg-slate-50/50 border border-slate-100 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none font-bold text-sm" 
        />
        <button 
          type="button" 
          @click="checkId" 
          class="px-4 h-11 rounded-xl font-bold text-[11px] transition-all border"
          :class="isIdAvailable 
            ? 'bg-blue-50 border-blue-200 text-blue-600' 
            : 'bg-white border-slate-200 text-slate-500 hover:bg-slate-50'"
        >
          {{ isIdAvailable ? '확인됨' : '중복확인' }}
        </button>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-4 animate-stagger-2">
      <input v-model="form.password" type="password" placeholder="비밀번호" class="w-full h-11 px-4 rounded-xl bg-slate-50/50 border border-slate-100 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none font-bold text-sm" />
      
      <div class="relative">
        <input v-model="form.passwordConfirm" type="password" placeholder="비밀번호 확인" 
               class="w-full h-11 px-4 rounded-xl bg-slate-50/50 border border-slate-100 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none font-bold text-sm" 
               :class="{'ring-1 ring-red-100': form.passwordConfirm && !isPasswordMatch, 'ring-1 ring-green-100': isPasswordMatch}" />
        
        <span v-if="form.passwordConfirm && !isPasswordMatch" class="absolute -bottom-5 left-1 text-[10px] text-red-500 font-bold">불일치</span>
        <span v-if="isPasswordMatch" class="absolute -bottom-5 left-1 text-[10px] text-green-500 font-bold">일치!</span>
      </div>
    </div>

    <div class="space-y-4 animate-stagger-3 mt-4">
      <input v-model="form.email" type="email" placeholder="이메일" class="w-full h-11 px-4 rounded-xl bg-slate-50/50 border border-slate-100 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none font-bold text-sm" />
      
      <div class="flex gap-2">
        <input 
          v-model="form.nickname" 
          type="text" 
          placeholder="닉네임" 
          @input="isNicknameAvailable = false"
          class="flex-1 h-11 px-4 rounded-xl bg-slate-50/50 border border-slate-100 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none font-bold text-sm" 
        />
        <button 
          type="button" 
          @click="checkNickname" 
          class="px-4 h-11 rounded-xl font-bold text-[11px] transition-all border"
          :class="isNicknameAvailable 
            ? 'bg-blue-50 border-blue-200 text-blue-600' 
            : 'bg-white border-slate-200 text-slate-500 hover:bg-slate-50'"
        >
          {{ isNicknameAvailable ? '확인됨' : '중복확인' }}
        </button>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <input v-model="form.name" placeholder="실명" class="h-11 px-4 rounded-xl bg-slate-50/50 border border-slate-100 font-bold text-sm outline-none" />
        <input v-model="form.birth_date" type="date" class="h-11 px-4 rounded-xl bg-slate-50/50 border border-slate-100 font-bold text-sm text-slate-500 outline-none" />
      </div>
    </div>

    <div class="pt-6 animate-stagger-4">
      <button 
        type="submit" 
        :disabled="authStore.isLoading"
        class="w-full h-12 rounded-xl bg-slate-900 hover:bg-blue-600 text-white font-bold shadow-xl shadow-slate-200 transition-all active:scale-[0.97] disabled:bg-slate-400"
      >
        <span v-if="authStore.isLoading" class="loading loading-spinner loading-xs"></span>
        <span v-else>회원가입 완료 🐜</span>
      </button>
    </div>
  </form>
</template>