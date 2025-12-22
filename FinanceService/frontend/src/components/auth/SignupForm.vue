<script setup>
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Label from '@/components/ui/label/Label.vue'
import Input from '@/components/ui/input/Input.vue'
import Button from '@/components/ui/button/Button.vue'

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
  birth_date: null // 🐜 DateField는 null이나 'YYYY-MM-DD' 형식
})

// --- 중복 확인 로직 ---
const checkId = async () => {
  if (!form.username) return alert('아이디를 입력해주세요.')
  const result = await authStore.checkUsername(form.username)
  isIdAvailable.value = result.available
  alert(result.message)
}

const checkNickname = async () => {
  if (!form.nickname) return alert('닉네임을 입력해주세요.')
  const result = await authStore.checkNickname(form.nickname)
  isNicknameAvailable.value = result.available
  alert(result.message)
}

const setNicknameAsId = async () => {
  if (!isIdAvailable.value) return alert('아이디 중복 확인을 먼저 완료해주세요.')
  form.nickname = form.username
  // 🐜 아이디가 사용 가능하다면 닉네임으로서의 중복 확인도 서버에 한 번 더 물어보는 게 안전해
  const result = await authStore.checkNickname(form.nickname)
  isNicknameAvailable.value = result.available
  if (result.available) alert('아이디와 동일한 닉네임으로 설정되었습니다. ✨')
}

const onSubmit = () => {
  if (!isIdAvailable.value) return alert('아이디 중복 확인이 필요합니다.')
  if (!isNicknameAvailable.value) return alert('닉네임 중복 확인이 필요합니다.')
  if (form.password !== form.passwordConfirm) return alert('비밀번호가 일치하지 않습니다.')
  
  // 🐜 부모 컴포넌트로 데이터 전송
  emit('submit', { ...form })
}
</script>

<template>
  <form @submit.prevent="onSubmit" class="space-y-10 pt-2">
    
    <div class="space-y-6 animate-stagger-1">
      <div class="flex items-center gap-2 mb-2">
        <div class="w-1 h-4 bg-blue-600 rounded-full"></div>
        <h3 class="text-sm font-black text-slate-800 uppercase tracking-tighter">계정 설정</h3>
      </div>

      <div class="space-y-2">
        <Label class="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">아이디</Label>
        <div class="flex gap-2">
          <Input v-model="form.username" placeholder="아이디" @input="isIdAvailable = false"
                 class="h-11 rounded-xl bg-slate-50/50 border-slate-100 focus-visible:ring-blue-600 transition-all flex-1" />
          <Button type="button" @click="checkId" variant="outline" 
                  :class="isIdAvailable ? 'text-blue-600 border-blue-100 bg-blue-50' : ''"
                  class="h-11 px-4 rounded-xl text-xs font-bold border-slate-200 transition-all">
            {{ isIdAvailable ? '확인됨' : '중복 확인' }}
          </Button>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <Input v-model="form.password" type="password" placeholder="비밀번호" class="h-11 rounded-xl bg-slate-50/50 border-slate-100 focus-visible:ring-blue-600" />
        <Input v-model="form.passwordConfirm" type="password" placeholder="비밀번호 확인" class="h-11 rounded-xl bg-slate-50/50 border-slate-100 focus-visible:ring-blue-600" />
      </div>
      <Input v-model="form.email" type="email" placeholder="이메일 (email@ants.com)" class="h-11 rounded-xl bg-slate-50/50 border-slate-100" />
    </div>

    <div class="py-2 animate-stagger-2">
      <div class="h-px bg-slate-100 w-full"></div>
    </div>

    <div class="space-y-6 animate-stagger-3">
      <div class="flex items-center gap-2 mb-2">
        <div class="w-1 h-4 bg-blue-600 rounded-full"></div>
        <h3 class="text-sm font-black text-slate-800 uppercase tracking-tighter">프로필 정보</h3>
      </div>

      <div class="space-y-2">
        <Label class="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">닉네임</Label>
        <div class="flex flex-col gap-2">
          <Input v-model="form.nickname" placeholder="닉네임" @input="isNicknameAvailable = false"
                 class="h-11 rounded-xl bg-slate-50/50 border-slate-100 focus-visible:ring-blue-600 transition-all w-full" />
          <div class="grid grid-cols-2 gap-2">
            <Button type="button" @click="setNicknameAsId" variant="outline" 
                    class="h-10 rounded-xl text-[11px] font-bold border-slate-200 hover:bg-slate-50 transition-all">
              아이디와 동일
            </Button>
            <Button type="button" @click="checkNickname" variant="outline" 
                    :class="isNicknameAvailable ? 'text-blue-600 border-blue-100 bg-blue-50' : ''"
                    class="h-10 rounded-xl text-[11px] font-bold border-slate-200 transition-all">
              {{ isNicknameAvailable ? '확인됨' : '중복 확인' }}
            </Button>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <Input v-model="form.name" placeholder="실명" class="h-11 rounded-xl bg-slate-50/50 border-slate-100" />
        <Input v-model="form.birth_date" type="date" class="h-11 rounded-xl bg-slate-50/50 border-slate-100 text-slate-400" />
      </div>
      <Input v-model="form.phone_number" placeholder="연락처 (010-0000-0000)" class="h-11 rounded-xl bg-slate-50/50 border-slate-100" />
    </div>

    <div class="pt-8 animate-stagger-4">
      <Button type="submit" 
              class="w-full h-12 rounded-xl bg-slate-900 hover:bg-blue-600 text-white font-bold shadow-xl shadow-slate-200 transition-all active:scale-[0.97]">
        회원가입 완료 🐜
      </Button>
    </div>
  </form>
</template>

<style scoped>
/* 🐜 Expo-out 슬라이드업 애니메이션 */
[class^="animate-stagger-"] {
  opacity: 0;
  animation: slideUpStagger 1s cubic-bezier(0.19, 1, 0.22, 1) forwards;
}
.animate-stagger-1 { animation-delay: 0.1s; }
.animate-stagger-2 { animation-delay: 0.3s; }
.animate-stagger-3 { animation-delay: 0.5s; }
.animate-stagger-4 { animation-delay: 0.7s; }

@keyframes slideUpStagger {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}

:deep(.focus-visible\:ring-blue-600) {
  --tw-ring-color: rgb(37 99 235);
}
</style>