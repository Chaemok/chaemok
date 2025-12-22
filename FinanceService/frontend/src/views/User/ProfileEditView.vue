<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

// 🐜 기존 유저 데이터로 초기값 세팅
const editForm = ref({ ...authStore.user })

const handleUpdate = async () => {
  const success = await authStore.updateProfile(editForm.value)
  if (success) {
    alert('수정이 완료되었습니다! 🐜')
    router.push('/profile')
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto py-12 px-4">
    <div class="bg-white rounded-[32px] p-8 border border-slate-100 shadow-sm">
      <h2 class="text-xl font-black mb-8">프로필 수정 🐜</h2>
      <div class="grid gap-6">
        <div class="flex flex-col gap-2">
          <label class="text-sm font-bold text-slate-500">닉네임</label>
          <input v-model="editForm.nickname" class="input input-bordered rounded-2xl h-14 font-bold" />
        </div>
        <div class="flex flex-col gap-2">
          <label class="text-sm font-bold text-slate-500">운용 자산</label>
          <input v-model.number="editForm.money" type="number" class="input input-bordered rounded-2xl h-14 font-bold" />
        </div>
        </div>
      <div class="flex gap-4 mt-10">
        <button @click="$router.back()" class="btn flex-1 rounded-2xl h-14 font-bold">취소</button>
        <button @click="handleUpdate" class="btn btn-primary flex-1 rounded-2xl h-14 font-bold text-white">저장하기</button>
      </div>
    </div>
  </div>
</template>