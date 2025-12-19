<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import axios from 'axios'

// 1. 컴포넌트 임포트
import PageHeader from '@/components/layout/PageHeader.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import UserAvatar from '@/components/common/UserAvatar.vue'
import ProfileInfoRow from '@/components/common/ProfileInfoRow.vue' // [추가됨]

const store = useUserStore()
const router = useRouter()

const userInfo = ref({
  username: '',
  email: '',
  nickname: '',
  name: '',
  money: 0,
  salary: 0,
  job: '',
  profile_image: null
})

const formatMoney = (val) => val ? val.toLocaleString() : '0'

// onMounted(() => {
//   axios({
//     method: 'get',
//     url: `${store.API_URL}/api/accounts/me/`,
//     headers: { Authorization: `Bearer ${store.token}` }
//   })
//   .then((res) => {
//     userInfo.value = res.data
//     store.nickname = res.data.nickname
//     store.profileImage = res.data.profile_image
//   })
//   .catch((err) => console.log(err))
// })
onMounted(() => {
  // 1. [디버깅] 스토어에 토큰이 진짜 있는지 확인
  console.log('① 현재 저장된 토큰:', store.token) 

  if (!store.token) {
    alert('로그인 정보가 없습니다. 로그인 페이지로 이동합니다.')
    router.push({ name: 'login' })
    return
  }

  axios({
    method: 'get',
    url: `${store.API_URL}/api/accounts/me/`,
    // 주의: DRF 설정에 따라 'Bearer'가 아니라 'Token'일 수도 있습니다.
    headers: { Authorization: `Bearer ${store.token}` }
  })
  .then((res) => {
    // 2. [디버깅] 서버가 보내준 데이터 눈으로 확인
    console.log('② 서버 응답 데이터(res.data):', res.data)
    
    // 3. 데이터 넣기
    userInfo.value = res.data

    // 4. 스토어 정보 업데이트 (선택)
    store.nickname = res.data.nickname
    store.profileImage = res.data.profile_image
  })
  .catch((err) => {
    // 5. [디버깅] 에러가 났다면 왜 났는지 확인
    console.error('③ 데이터 로딩 실패:', err)
    if (err.response) {
      console.log('응답 상태 코드:', err.response.status) // 401이면 토큰/인증 문제, 404면 주소 틀림
      console.log('에러 메시지:', err.response.data)
    }
  })
})
const deleteAccount = () => {
  if (confirm('정말로 탈퇴하시겠습니까? \n탈퇴 시 모든 정보가 삭제되며 복구할 수 없습니다.')) {
    axios({
      method: 'delete',
      url: `${store.API_URL}/api/accounts/me/`, 
      headers: { Authorization: `Bearer ${store.token}` }
    })
    .then(() => {
      alert('회원 탈퇴가 완료되었습니다.')
      store.logOut() 
    })
    .catch(err => {
      console.error(err)
      alert('탈퇴 처리에 실패했습니다.')
    })
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 py-8 mb-20">
    <PageHeader title="👤 내 정보 상세" subtitle="등록된 회원 정보를 확인합니다." />

    <BaseCard class="mb-6">
      
      <div class="flex flex-col md:flex-row items-start gap-8">
        <div class="flex-shrink-0 mx-auto md:mx-0">
          <UserAvatar 
            :image="userInfo.profile_image" 
            :name="userInfo.username" 
            sizeClass="w-32 h-32 text-4xl shadow-md border-4 border-gray-50" 
          />
        </div>

        <div class="flex-grow w-full space-y-5">
           <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-6">
             
             <ProfileInfoRow label="아이디" :value="userInfo.username" />
             <ProfileInfoRow label="이름" :value="userInfo.name" />
             <ProfileInfoRow label="닉네임" :value="userInfo.nickname" />
             
             <ProfileInfoRow label="직업">
                <span class="badge badge-primary badge-outline">{{ userInfo.job || '미입력' }}</span>
             </ProfileInfoRow>

             <ProfileInfoRow label="이메일" :value="userInfo.email" class="sm:col-span-2" />

           </div>
        </div>
      </div>

      <div class="divider my-6"></div>

      <div class="grid grid-cols-2 gap-4 bg-gray-50 p-5 rounded-2xl border border-gray-100">
         <div class="text-center">
           <label class="text-xs text-gray-500 font-bold block mb-1">보유 자산</label>
           <div class="font-bold text-xl text-blue-600">{{ formatMoney(userInfo.money) }}원</div>
         </div>
         <div class="text-center border-l border-gray-200">
           <label class="text-xs text-gray-500 font-bold block mb-1">연봉</label>
           <div class="font-bold text-xl text-indigo-600">{{ formatMoney(userInfo.salary) }}원</div>
         </div>
      </div>

      <div class="-mx-6 -mb-6 md:-mx-8 md:-mb-8 mt-8 px-6 py-4 md:px-8 bg-gray-50 border-t border-gray-100 flex flex-wrap justify-between items-center gap-3">
        <button 
          @click="deleteAccount"
          class="text-sm text-gray-400 hover:text-red-500 underline transition-colors"
        >
          회원 탈퇴
        </button>
        
        <div class="flex gap-2">
          <BaseButton color="white" @click="router.push({ name: 'mypage' })">
            뒤로가기
          </BaseButton>
          <BaseButton color="blue" @click="router.push({ name: 'profile-edit' })">
            정보 수정
          </BaseButton>
        </div>
      </div>

    </BaseCard>
  </div>
</template>