<script setup>
import { useAuthStore } from '@/stores/auth'
import ProfileHero from '@/components/profile/ProfileHero.vue' 
// import AssertChartCard from '@/components/profile/AssertChartCard.vue' // 필요시 주석 해제

const authStore = useAuthStore()

const riskLabels = {
  1: '안정형', 2: '안정추구형', 3: '위험중립형', 4: '적극투자형', 5: '공격투자형'
}
</script>

<template>
  <div class="max-w-4xl mx-auto py-10 px-4" v-if="authStore.user">
    <ProfileHero :user="authStore.user" />
    
    <div class="flex justify-end gap-2 mt-4">
        <router-link to="/profile" class="btn bg-slate-900 text-white rounded-xl font-bold">
          개인정보 상세
        </router-link>
        <router-link to="/profile/edit" class="btn btn-ghost bg-slate-50 rounded-xl font-bold text-slate-600">
          프로필 수정
        </router-link>
    </div>
  </div>
  
  <div v-else class="text-center py-20">
    <p class="text-slate-400">데이터를 불러오는 중입니다... 🐜</p>
  </div>
</template>