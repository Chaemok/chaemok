<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import ProfileEditForm from '@/components/profile/ProfileEditForm.vue' // ✅ 컴포넌트 import

const authStore = useAuthStore()
const router = useRouter()

// 폼에서 'submit' 이벤트가 올라오면 실행
const handleUpdate = async (updatedData) => {
  // 스토어의 updateProfile 액션 호출 (없으면 axios 직접 호출로 대체 가능)
  // 여기선 authStore에 기능이 있다고 가정하거나, 아래처럼 직접 구현
  try {
    const success = await authStore.updateProfile(updatedData)
    if (success) {
      alert('✅ 프로필이 성공적으로 수정되었습니다!')
      router.push('/mypage')
    } else {
      // 스토어에서 실패 리턴 시
      alert('수정에 실패했습니다. 잠시 후 다시 시도해주세요.')
    }
  } catch (err) {
    console.error(err)
    alert('오류가 발생했습니다.')
  }
}
</script>

<template>
  <div class="max-w-xl mx-auto py-12 px-6">
    <div class="bg-white rounded-[32px] p-8 md:p-10 border border-slate-100 shadow-xl">
      <div class="mb-8">
        <h2 class="text-2xl font-black text-slate-800 mb-2">프로필 수정 🐜</h2>
        <p class="text-sm text-slate-500 font-bold">정확한 추천을 위해 정보를 최신화해주세요.</p>
      </div>

      <ProfileEditForm 
        v-if="authStore.user" 
        :initial-data="authStore.user" 
        @submit="handleUpdate" 
      />
    </div>
  </div>
</template>