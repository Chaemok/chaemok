<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import UserAvatar from '@/components/auth/UserAvatar.vue'
import UserProfile from '@/components/auth/UserProfile.vue'

const authStore = useAuthStore()
const isMobileMenuOpen = ref(false)

// 🐜 가나다순으로 정렬된 메뉴 리스트
const navLinks = [
  { name: '은행/증권사 찾기', path: '/map' },
  { name: '예/적금 추천', path: '/deposit' },
  { name: '실시간 환율', path: '/exchange' },
  { name: '주식 추천', path: '/stocks' },
  { name: '커뮤니티', path: '/community' },
]

const toggleMenu = () => { isMobileMenuOpen.value = !isMobileMenuOpen.value }
const closeMenu = () => { isMobileMenuOpen.value = false }
</script>

<template>
  <nav class="sticky top-0 z-[100] w-full border-b border-slate-100 bg-white/90 backdrop-blur-xl">
    <div class="max-w-6xl mx-auto px-4 h-20 flex items-center justify-between">
      
      <div class="flex-shrink-0">
        <router-link to="/" class="flex items-center gap-2 group" @click="closeMenu">
          <span class="text-2xl transition-transform group-hover:scale-125">🐜</span>
          <span class="text-xl font-black text-slate-800 tracking-tighter">
            Smart <span class="text-blue-600 font-black">Ants</span>
          </span>
        </router-link>
      </div>

      <div class="hidden lg:flex items-center gap-2">
        <ul class="flex items-center gap-1">
          <li v-for="link in navLinks" :key="link.path">
            <router-link :to="link.path" 
              class="text-[13px] font-black text-slate-500 hover:text-blue-600 hover:bg-blue-50 rounded-xl px-4 py-2 transition-all"
              active-class="text-blue-600 bg-blue-50">
              {{ link.name }}
            </router-link>
          </li>
        </ul>
      </div>

      <div class="flex items-center gap-3">
        <div v-if="!authStore.isLoggedIn" class="hidden sm:flex gap-2">
          <router-link to="/login" class="text-sm font-bold text-slate-500 px-4 py-2">로그인</router-link>
          <router-link to="/signup" class="bg-blue-600 text-white text-sm font-black px-5 py-2 rounded-xl shadow-lg shadow-blue-100">시작하기</router-link>
        </div>
        
        <div v-if="authStore.isLoggedIn" class="dropdown dropdown-end">
          <label tabindex="0" class="btn btn-ghost btn-circle p-0 min-h-0 h-10 w-10">
            <UserAvatar 
              :image="authStore.user?.profile_image" 
              :name="authStore.user?.nickname || 'Ant'" 
              sizeClass="w-9 h-9"
            />
          </label>
          <ul tabindex="0" class="dropdown-content mt-4 p-4 shadow-2xl bg-white rounded-[2rem] w-64 border border-slate-50 animate-in fade-in zoom-in-95 duration-200">
            <li class="px-2 py-4 border-b border-slate-50 mb-2 pointer-events-none">
              <UserProfile :user="authStore.user" />
            </li>
            <li><router-link to="/mypage" class="block rounded-xl py-3 px-4 font-bold text-slate-600 hover:bg-slate-50">내 프로필</router-link></li>
            <li><router-link to="/settings" class="block rounded-xl py-3 px-4 font-bold text-slate-600 hover:bg-slate-50">계정 설정</router-link></li>
            <li class="mt-2 pt-2 border-t border-slate-50">
              <a @click="authStore.logout" class="block rounded-xl py-3 px-4 text-red-500 font-black hover:bg-red-50 cursor-pointer">로그아웃</a>
            </li>
          </ul>
        </div>

        <button @click="toggleMenu" 
          class="lg:hidden flex items-center justify-center w-10 h-10 text-slate-600 focus:outline-none z-[110]"
          aria-label="Toggle Menu">
          <div class="w-6 h-5 relative flex flex-col justify-between">
            <span class="w-full h-0.5 bg-current rounded-full transition-all duration-300" :class="isMobileMenuOpen ? 'rotate-45 translate-y-2' : ''"></span>
            <span class="w-full h-0.5 bg-current rounded-full transition-all duration-300" :class="isMobileMenuOpen ? 'opacity-0' : ''"></span>
            <span class="w-full h-0.5 bg-current rounded-full transition-all duration-300" :class="isMobileMenuOpen ? '-rotate-45 -translate-y-2' : ''"></span>
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
    <div v-if="isMobileMenuOpen" class="fixed inset-0 bg-white z-[95] lg:hidden pt-24 px-8 flex flex-col gap-10">
      <div class="space-y-4">
        <p class="text-[11px] font-black text-slate-300 uppercase tracking-widest ml-4">Financial Menu</p>
        <div class="flex flex-col gap-2">
          <router-link v-for="link in navLinks" :key="link.path" :to="link.path" @click="closeMenu"
            class="flex items-center justify-between p-5 rounded-[1.8rem] bg-slate-50 text-slate-800 text-xl font-black active:bg-blue-50 active:text-blue-600 transition-all"
            active-class="bg-blue-50 text-blue-600">
            {{ link.name }}
            <span class="text-slate-300">→</span>
          </router-link>
        </div>
      </div>

      <div v-if="!authStore.isLoggedIn" class="mt-auto mb-12 flex flex-col gap-3">
        <router-link to="/signup" @click="closeMenu" class="btn h-16 bg-blue-600 text-white border-none rounded-[1.5rem] text-lg font-black shadow-xl shadow-blue-100">🐜 시작하기</router-link>
        <router-link to="/login" @click="closeMenu" class="btn h-16 btn-ghost rounded-[1.5rem] font-bold text-slate-400 text-lg">로그인</router-link>
      </div>
    </div>
  </transition>
</template>

<style scoped>
/* 🐜 모바일 메뉴 오픈 시 배경 스크롤을 막고 싶다면 HomeView 등 부모에서 처리 권장 */
</style>