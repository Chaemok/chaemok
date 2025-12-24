<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import UserAvatar from '@/components/auth/UserAvatar.vue'
import UserProfile from '@/components/auth/UserProfile.vue'

const authStore = useAuthStore()
const isMobileMenuOpen = ref(false)

// 🐜 메뉴 리스트 (YouTube 추가됨)
const navLinks = [
  { name: '은행 찾기', path: '/map' },
  { name: '예/적금 상품', path: '/deposit' },
  { name: '환율 계산', path: '/exchange-rate' },
  { name: '주식 추천', path: '/stocks' },
  { name: '금/은 시세', path: '/spot' },
  { name: 'YouTube', path: '/youtube', isSpecial: true }, // 🔴 Special 플래그 추가
  { name: '커뮤니티', path: '/community' },
]

const toggleMenu = () => { isMobileMenuOpen.value = !isMobileMenuOpen.value }
const closeMenu = () => { isMobileMenuOpen.value = false }
</script>

<template>
  <nav class="sticky top-0 z-[100] w-full border-b border-slate-200/60 bg-white/80 backdrop-blur-md transition-all duration-300">
    <div class="max-w-7xl mx-auto px-4 h-[4.5rem] flex items-center justify-between">
      
      <div class="flex-shrink-0">
        <router-link to="/" class="flex items-center gap-2 group" @click="closeMenu">
          <span class="text-2xl transition-transform duration-300 group-hover:-rotate-12 group-hover:scale-110">🐜</span>
          <span class="text-xl font-black tracking-tighter text-slate-800">
            Smart<span class="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent ml-0.5">Ants</span>
          </span>
        </router-link>
      </div>

      <div class="hidden lg:flex items-center gap-1">
        <ul class="flex items-center p-1 bg-slate-100/50 rounded-full border border-slate-200/50">
          <li v-for="link in navLinks" :key="link.path">
            <router-link :to="link.path" 
              class="relative px-5 py-2.5 rounded-full text-[13px] font-bold transition-all duration-300 ease-out"
              :class="[
                link.isSpecial 
                  ? 'text-slate-600 hover:text-red-600 hover:bg-white hover:shadow-sm' 
                  : 'text-slate-500 hover:text-blue-600 hover:bg-white hover:shadow-sm'
              ]"
              active-class="!bg-white !shadow-md !text-slate-900 scale-105"
            >
              <span v-if="link.isSpecial" class="mr-1 text-red-500">▶</span>
              {{ link.name }}
            </router-link>
          </li>
        </ul>
      </div>

      <div class="flex items-center gap-3">
        <div v-if="!authStore.isLoggedIn" class="hidden sm:flex items-center gap-2">
          <router-link to="/login" class="text-sm font-bold text-slate-500 hover:text-slate-800 px-4 py-2 transition-colors">로그인</router-link>
          <router-link to="/signup" class="bg-slate-900 hover:bg-slate-800 text-white text-sm font-bold px-5 py-2.5 rounded-full shadow-lg shadow-slate-200 transition-all hover:-translate-y-0.5">
            시작하기
          </router-link>
        </div>
        
        <div v-if="authStore.isLoggedIn" class="dropdown dropdown-end">
          <label tabindex="0" class="btn btn-ghost btn-circle p-0 min-h-0 h-11 w-11 border border-slate-100 hover:bg-slate-50 transition-all">
            <UserAvatar 
              :image="authStore.user?.profile_image" 
              :name="authStore.user?.nickname || 'Ant'" 
              sizeClass="w-9 h-9"
            />
          </label>
          <ul tabindex="0" class="dropdown-content mt-4 p-3 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.1)] bg-white rounded-[2rem] w-72 border border-slate-100 animate-in fade-in zoom-in-95 duration-200">
            <li class="p-2 mb-2 pointer-events-none">
              <UserProfile :user="authStore.user" />
            </li>
            <div class="h-px bg-slate-100 my-1 mx-2"></div>
            <li><router-link to="/mypage" class="rounded-xl py-3 px-4 font-bold text-slate-600 hover:bg-slate-50 hover:text-blue-600 transition-colors">👤 내 프로필</router-link></li>
            <li><router-link to="/settings" class="rounded-xl py-3 px-4 font-bold text-slate-600 hover:bg-slate-50 hover:text-blue-600 transition-colors">⚙️ 계정 설정</router-link></li>
            <div class="h-px bg-slate-100 my-1 mx-2"></div>
            <li>
              <a @click="authStore.logout" class="rounded-xl py-3 px-4 text-rose-500 font-bold hover:bg-rose-50 cursor-pointer flex justify-between group">
                로그아웃 
                <span class="group-hover:translate-x-1 transition-transform">→</span>
              </a>
            </li>
          </ul>
        </div>

        <button @click="toggleMenu" 
          class="lg:hidden flex items-center justify-center w-10 h-10 text-slate-800 focus:outline-none z-[110]"
          aria-label="Toggle Menu">
          <div class="w-6 h-5 relative flex flex-col justify-between">
            <span class="w-full h-0.5 bg-current rounded-full transition-all duration-300 origin-right" :class="isMobileMenuOpen ? '-rotate-45 -translate-y-1 w-6' : ''"></span>
            <span class="w-full h-0.5 bg-current rounded-full transition-all duration-300" :class="isMobileMenuOpen ? 'opacity-0 scale-0' : ''"></span>
            <span class="w-full h-0.5 bg-current rounded-full transition-all duration-300 origin-right" :class="isMobileMenuOpen ? 'rotate-45 translate-y-1 w-6' : ''"></span>
          </div>
        </button>
      </div>
    </div>
  </nav>

  <transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="translate-x-full opacity-0"
    enter-to-class="translate-x-0 opacity-100"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="translate-x-0 opacity-100"
    leave-to-class="translate-x-full opacity-0"
  >
    <div v-if="isMobileMenuOpen" class="fixed inset-0 bg-white/95 backdrop-blur-xl z-[95] lg:hidden pt-28 px-6 flex flex-col">
      <div class="space-y-6">
        <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] ml-2">Navigation</p>
        <div class="flex flex-col gap-3">
          <router-link v-for="link in navLinks" :key="link.path" :to="link.path" @click="closeMenu"
            class="flex items-center justify-between p-4 rounded-2xl text-xl font-bold transition-all duration-200"
            :class="[
               link.isSpecial 
               ? 'text-slate-800 hover:bg-red-50 hover:text-red-600 active:bg-red-50 active:text-red-600' 
               : 'text-slate-800 hover:bg-blue-50 hover:text-blue-600 active:bg-blue-50 active:text-blue-600'
            ]"
            active-class="!bg-slate-100"
          >
            <div class="flex items-center gap-3">
              <span v-if="link.isSpecial" class="text-red-500">📺</span>
              {{ link.name }}
            </div>
            <span class="text-slate-300 text-2xl">›</span>
          </router-link>
        </div>
      </div>

      <div v-if="!authStore.isLoggedIn" class="mt-auto mb-10 flex flex-col gap-3">
        <router-link to="/signup" @click="closeMenu" class="btn h-14 bg-slate-900 text-white border-none rounded-2xl text-lg font-bold shadow-xl shadow-slate-200">
          🐜 SmartAnts 시작하기
        </router-link>
        <router-link to="/login" @click="closeMenu" class="btn h-14 btn-ghost rounded-2xl font-bold text-slate-500 text-lg">
          이미 계정이 있어요
        </router-link>
      </div>
    </div>
  </transition>
</template>

<style scoped>
/* 드롭다운 애니메이션 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: fadeIn 0.2s ease-out forwards; }
</style>