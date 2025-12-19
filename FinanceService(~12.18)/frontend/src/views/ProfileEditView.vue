<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import axios from 'axios'

// 컴포넌트 임포트
import PageHeader from '@/components/layout/PageHeader.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import JobSelector from '@/components/JobSelector.vue' // 직업 선택 컴포넌트

const store = useUserStore()
const router = useRouter()

const username = ref('') // 읽기 전용
const name = ref('')     // 읽기 전용
const nickname = ref('')
const email = ref('')
const birthDate = ref('')
const money = ref(0)
const salary = ref(0)
const job = ref('')
const profileImage = ref(null)

// 1. 최신 데이터 가져오기
onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/accounts/me/`,
    headers: { Authorization: `Bearer ${store.token}` }
  })
  .then((res) => {
    username.value = res.data.username
    name.value = res.data.name
    nickname.value = res.data.nickname
    email.value = res.data.email
    birthDate.value = res.data.birth_date
    money.value = res.data.money
    salary.value = res.data.salary
    job.value = res.data.job
  })
  .catch((err) => console.log(err))
})

const handleFileUpload = (event) => {
  profileImage.value = event.target.files[0]
}

const checkNickname = () => {
  if (!nickname.value) return
  store.checkNickname(nickname.value)
    .then((res) => {
      alert(res.data.message)
    })
}

// 2. 수정 요청 (FormData 사용)
const updateProfile = () => {
  const formData = new FormData()
  // username, name은 수정 불가하므로 안 보냄
  formData.append('nickname', nickname.value)
  formData.append('email', email.value)
  if (birthDate.value) formData.append('birth_date', birthDate.value)
  if (money.value) formData.append('money', money.value)
  if (salary.value) formData.append('salary', salary.value)
  if (job.value) formData.append('job', job.value)
  
  if (profileImage.value) {
    formData.append('profile_image', profileImage.value)
  }

  store.updateProfile(formData)
  // store에서 이동 처리가 없다면 여기서 .then(() => router.push({ name: 'profile' })) 추가
}

const changePassword = () => {
  const oldPw = prompt("현재 비밀번호")
  if (!oldPw) return
  const newPw = prompt("새 비밀번호")
  if (!newPw) return
  const newPwConfirm = prompt("새 비밀번호 확인")
  if (newPw !== newPwConfirm) return alert("불일치")

  axios({
    method: 'post',
    url: `${store.API_URL}/api/accounts/password/change/`,
    headers: { Authorization: `Bearer ${store.token}` },
    data: { old_password: oldPw, new_password: newPw, new_password_confirm: newPwConfirm }
  })
  .then(() => {
    alert("비밀번호 변경 완료. 다시 로그인해주세요.")
    store.logOut()
  })
  .catch(err => alert(err.response?.data?.error || "실패"))
}
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 py-8">
    <PageHeader title="⚙️ 회원 정보 수정" subtitle="최신 정보를 입력하면 더 정확한 추천을 받을 수 있습니다." />

    <BaseCard>
      <div class="space-y-5">
        <h3 class="font-bold text-lg border-b pb-2">기본 정보</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
           <div>
             <label class="label font-bold text-sm">아이디</label>
             <input type="text" :value="username" disabled class="input input-bordered w-full bg-gray-100 text-gray-500" />
           </div>
           <div>
             <label class="label font-bold text-sm">이름</label>
             <input type="text" :value="name" disabled class="input input-bordered w-full bg-gray-100 text-gray-500" />
           </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="label font-bold text-sm">닉네임</label>
              <div class="flex gap-2">
                <input type="text" v-model="nickname" class="input input-bordered w-full" />
                <BaseButton type="button" color="gray" size="sm" @click="checkNickname">확인</BaseButton>
              </div>
            </div>
             <div>
              <label class="label font-bold text-sm">이메일</label>
              <input type="email" v-model="email" class="input input-bordered w-full" />
            </div>
        </div>

        <div>
          <label class="label font-bold text-sm">프로필 사진 변경</label>
          <div class="flex items-center gap-4">
            <div v-if="store.profileImage" class="w-12 h-12 rounded-full overflow-hidden border bg-gray-50">
               <img :src="store.profileImage.startsWith('http') ? store.profileImage : `${store.API_URL}${store.profileImage}`" class="w-full h-full object-cover" />
            </div>
            <input type="file" @change="handleFileUpload" class="file-input file-input-bordered w-full" accept="image/*" />
          </div>
        </div>

        <h3 class="font-bold text-lg border-b pb-2 pt-4">상세 정보</h3>
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
             <div><label class="label font-bold text-sm">자산 (원)</label><input type="number" v-model="money" class="input input-bordered w-full" /></div>
             <div><label class="label font-bold text-sm">연봉 (원)</label><input type="number" v-model="salary" class="input input-bordered w-full" /></div>
         </div>

        <div class="flex justify-between items-center pt-4 mt-4 border-t border-gray-100">
          <BaseButton type="button" color="yellow" @click="changePassword">🔒 비밀번호 변경</BaseButton>
          <div class="flex gap-2">
            <BaseButton color="gray" @click="router.push({ name: 'profile' })">취소</BaseButton>
            <BaseButton color="blue" @click="updateProfile">저장하기</BaseButton>
          </div>
        </div>

      </div>
    </BaseCard>
  </div>
</template>