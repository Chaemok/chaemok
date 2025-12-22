<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import SecurityModal from '@/components/auth/SecurityModal.vue'

const authStore = useAuthStore()
const isVerified = ref(false)
const showModal = ref(true)

const onVerified = () => {
  isVerified.value = true
  showModal.value = false
}
</script>

<template>
  <div class="max-w-2xl mx-auto py-12 px-4">
    <SecurityModal :isOpen="showModal" @close="$router.push('/mypage')" @success="onVerified" />

    <div v-if="isVerified" class="animate-in fade-in slide-in-from-bottom-4">
      <h1 class="text-2xl font-black text-slate-900 mb-8">상세 회원정보 🔒</h1>
      <router-link to="/profile/edit" class="btn btn-primary w-full h-14 rounded-2xl font-bold mt-8">
        정보 수정하기
      </router-link>
    </div>
  </div>
</template>