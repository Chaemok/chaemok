<!-- frontend/src/views/SignUpView.vue -->
<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import JobSelector from '@/components/JobSelector.vue' // 👈 직업 선택 컴포넌트 사용

const store = useUserStore()

// 입력 데이터
const username = ref('')
const password = ref('')
const passwordConfirm = ref('')
const name = ref('') 
const email = ref('')
const nickname = ref('')
const birthDate = ref('')
const money = ref(null)
const salary = ref(null)
const job = ref('')
const profileImage = ref(null) 

// 중복 확인 상태
const isIdChecked = ref(false)
const idCheckMessage = ref('')
const isNicknameChecked = ref(false) 
const nicknameCheckMessage = ref('')
const isSameAsId = ref(false) 

// [아이디 중복 확인]
const checkId = function () {
  if (!username.value) {
    idCheckMessage.value = "아이디를 입력해주세요."
    isIdChecked.value = false
    return
  }
  store.checkUsername(username.value)
    .then((res) => {
      if (res.data.available) {
        isIdChecked.value = true
        idCheckMessage.value = "사용 가능한 아이디입니다."
      } else {
        isIdChecked.value = false
        idCheckMessage.value = "이미 사용 중인 아이디입니다."
      }
    })
    .catch(() => {
      isIdChecked.value = false
      idCheckMessage.value = "중복 확인 오류"
    })
}

// [닉네임 중복 확인]
const checkNickname = function () {
  if (!nickname.value) return
  store.checkNickname(nickname.value)
    .then((res) => {
      if (res.data.available) {
        isNicknameChecked.value = true
        nicknameCheckMessage.value = "사용 가능한 닉네임입니다."
      } else {
        isNicknameChecked.value = false
        nicknameCheckMessage.value = "이미 사용 중인 닉네임입니다."
      }
    })
}

// [아이디와 동일하게 사용]
const toggleSameAsId = () => {
  if (isSameAsId.value) {
    nickname.value = username.value
    if (isIdChecked.value) checkNickname()
  } else {
    nickname.value = ''
    isNicknameChecked.value = false
    nicknameCheckMessage.value = ''
  }
}

// [파일 업로드 처리]
const handleFileUpload = (event) => {
  profileImage.value = event.target.files[0]
}

// [회원가입 제출]
const signUp = function () {
  // 1. 유효성 검사
  if (password.value !== passwordConfirm.value) return alert("비밀번호가 일치하지 않습니다.")
  if (!isIdChecked.value) return alert("아이디 중복 확인을 해주세요.")
  if (!isNicknameChecked.value) return alert("닉네임 중복 확인을 해주세요.")

  const formData = new FormData()
  
  // 2. 필수 데이터 추가
  formData.append('username', username.value)
  formData.append('password', password.value)
  formData.append('password2', passwordConfirm.value) // 백엔드 필드명 주의!
  formData.append('name', name.value)
  formData.append('email', email.value)
  formData.append('nickname', nickname.value)

  // 3. 선택 데이터 안전하게 처리 (빈 값이면 안 보내거나, 기본값 0 처리)
  
  // 생년월일: 값이 있을 때만 보냄
  if (birthDate.value) {
    formData.append('birth_date', birthDate.value)
  }

  // 자산/연봉: 값이 있으면 숫자로 변환, 없으면 0으로 보냄 (빈 문자열 방지)
  // Number()를 쓰면 '1000' -> 1000, '' -> 0 이 됨
  formData.append('money', money.value ? Number(money.value) : 0)
  formData.append('salary', salary.value ? Number(salary.value) : 0)

  // 직업: 빈 문자열('')이 아닐 때만 보냄
  if (job.value && job.value !== '') {
    formData.append('job', job.value)
  }
  
  // 프로필 이미지: 파일이 있을 때만 보냄
  if (profileImage.value) {
    formData.append('profile_image', profileImage.value)
  }
  
  // 4. 스토어 액션 호출 (에러 처리 포함)
  store.signUp(formData)
    .catch(err => {
      // 400 에러의 정확한 원인을 알러트로 띄워줌
      console.error(err)
      if (err.response && err.response.data) {
        const errorMsg = JSON.stringify(err.response.data)
        alert(`가입 실패: ${errorMsg}`)
      } else {
        alert("회원가입 중 오류가 발생했습니다.")
      }
    })
}
</script>

<template>
  <div class="max-w-xl mx-auto mt-10 px-4 mb-20">
    <BaseCard>
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-gray-900">회원가입</h1>
        <p class="text-gray-500 text-sm mt-2">상세 정보를 입력하면 맞춤형 금융 상품을 추천해 드립니다.</p>
      </div>

      <form @submit.prevent="signUp" class="space-y-5">
        <h3 class="font-bold text-lg border-b pb-2">기본 정보 (필수)</h3>
        
        <div>
          <label class="label font-bold text-sm">아이디</label>
          <div class="join w-full">
            <input 
              type="text" 
              v-model="username" 
              class="input input-bordered join-item w-full focus:outline-none" 
              required 
              @input="isIdChecked = false; idCheckMessage=''" 
              placeholder="아이디를 입력하세요" 
            />
            <button 
              type="button" 
              class="btn btn-neutral join-item rounded-r-lg" 
              @click="checkId"
            >
              중복확인
            </button>
          </div>
          <p class="text-xs mt-1 ml-1 font-medium" :class="isIdChecked ? 'text-blue-600' : 'text-red-500'">
            {{ idCheckMessage || '&nbsp;' }}
          </p>
        </div>

        <div>
          <label class="label font-bold text-sm">이름 (실명)</label>
          <input type="text" v-model="name" class="input input-bordered w-full" placeholder="홍길동" required />
          <span class="text-xs text-gray-400 ml-1">실명은 가입 후 수정할 수 없습니다.</span>
        </div>

        <div>
          <label class="label font-bold text-sm">닉네임</label>
          <div class="form-control mb-1">
            <label class="cursor-pointer label justify-start gap-2 py-0">
              <input type="checkbox" class="checkbox checkbox-xs rounded-sm" v-model="isSameAsId" @change="toggleSameAsId" />
              <span class="label-text text-xs text-gray-500">아이디와 동일하게 사용</span>
            </label>
          </div>
          
          <div class="join w-full">
            <input 
              type="text" 
              v-model="nickname" 
              class="input input-bordered join-item w-full focus:outline-none" 
              :disabled="isSameAsId" 
              required 
              @input="isNicknameChecked = false; nicknameCheckMessage=''" 
              placeholder="별명" 
            />
            <button 
              type="button" 
              class="btn btn-neutral join-item rounded-r-lg" 
              @click="checkNickname" 
              :disabled="isSameAsId"
            >
              중복확인
            </button>
          </div>
          <p class="text-xs mt-1 ml-1 font-medium" :class="isNicknameChecked ? 'text-blue-600' : 'text-red-500'">
            {{ nicknameCheckMessage || '&nbsp;' }}
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="label font-bold text-sm">이메일</label>
            <input type="email" v-model="email" class="input input-bordered w-full" placeholder="email@example.com" required />
          </div>
          <div>
            <label class="label font-bold text-sm">프로필 사진 (선택)</label>
            <input type="file" @change="handleFileUpload" class="file-input file-input-bordered w-full" accept="image/*" />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="label font-bold text-sm">비밀번호</label>
            <input type="password" v-model="password" class="input input-bordered w-full" placeholder="********" required />
          </div>
          <div>
            <label class="label font-bold text-sm">비밀번호 확인</label>
            <input type="password" v-model="passwordConfirm" class="input input-bordered w-full" placeholder="********" required />
          </div>
        </div>

        <h3 class="font-bold text-lg border-b pb-2 mt-6">상세 정보 (선택)</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="label font-bold text-sm">생년월일</label>
            <input type="date" v-model="birthDate" class="input input-bordered w-full" />
          </div>
          <div>
            <JobSelector v-model="job" />
          </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="label font-bold text-sm">자산 (원)</label>
            <input type="number" v-model="money" class="input input-bordered w-full" placeholder="0" />
          </div>
          <div>
            <label class="label font-bold text-sm">연봉 (원)</label>
            <input type="number" v-model="salary" class="input input-bordered w-full" placeholder="0" />
          </div>
        </div>

        <div class="pt-6">
          <BaseButton color="blue" class="w-full py-3 text-lg shadow-lg font-bold">
            회원가입
          </BaseButton>
        </div>
      </form>
    </BaseCard>
  </div>
</template>