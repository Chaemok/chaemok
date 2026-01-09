<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import SecurityModal from '@/components/auth/SecurityModal.vue'

const authStore = useAuthStore()
const isVerified = ref(false)
const showModal = ref(true)

const handleVerify = async (password) => {
  const success = await authStore.verifyPassword(password)
  if (success) {
    isVerified.value = true
    showModal.value = false
  } else {
    alert('비밀번호가 일치하지 않습니다. 🐜')
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto py-12 px-4">
    <SecurityModal :isOpen="showModal" @close="$router.push('/mypage')" @confirm="handleVerify" />

    <div v-if="isVerified" class="animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h1 class="text-2xl font-black text-slate-900 mb-8">상세 회원정보 🔒</h1>
      
      <div class="bg-white rounded-[32px] border border-slate-100 shadow-sm p-8 space-y-6">
        <div v-for="(val, label) in {
          '이름(ID)': authStore.user?.username,
          '이메일': authStore.user?.email,
          '연락처': authStore.user?.phone_number || '미등록',
          '생년월일': authStore.user?.birth_date || '미등록'
        }" :key="label" class="flex justify-between border-b border-slate-50 pb-4">
          <span class="text-sm font-bold text-slate-400">{{ label }}</span>
          <span class="text-slate-800 font-black">{{ val }}</span>
        </div>
        
        <router-link to="/profile/edit" class="btn btn-primary w-full h-14 rounded-2xl font-bold mt-4">
          정보 수정하기
        </router-link>
      </div>
    </div>
  </div>
</template>