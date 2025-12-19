<script setup>
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()

const navLinks = [
  { name: '예/적금 추천', path: '/deposit' },
  { name: '실시간 환율', path: '/exchange' },
  { name: '주식 추천', path: '/stocks' },
  { name: '은행/증권사 찾기', path: '/map' },
  { name: '커뮤니티', path: '/community' },
]
</script>

<template>
  <nav class="sticky top-0 z-50 w-full border-b border-slate-100 bg-white/80 backdrop-blur-md">
    <div class="navbar max-w-6xl mx-auto px-4 h-20">
      <div class="flex-1">
        <router-link to="/" class="flex items-center gap-2 group">
          <span class="text-2xl transition-transform group-hover:scale-125">🐜</span>
          <span class="text-xl font-black text-slate-800 tracking-tighter">
            Smart <span class="text-primary">Ants</span>
          </span>
        </router-link>
      </div>

      <div class="flex-none hidden lg:block">
        <ul class="menu menu-horizontal px-1 gap-2">
          <li v-for="link in navLinks" :key="link.path">
            <router-link :to="link.path" 
              class="text-sm font-bold text-slate-500 hover:text-primary hover:bg-indigo-50 rounded-xl px-4 py-2 transition-all"
              active-class="text-primary bg-indigo-50">
              {{ link.name }}
            </router-link>
          </li>
        </ul>
      </div>

      <div class="flex-none gap-4 ml-4">
        <div v-if="!authStore.isLoggedIn" class="flex gap-2">
          <router-link to="/login" class="btn btn-ghost btn-sm text-slate-500 hover:bg-slate-100 rounded-xl">로그인</router-link>
          <router-link to="/signup" class="btn btn-primary btn-sm text-white px-5 rounded-xl shadow-md shadow-primary/20">시작하기</router-link>
        </div>
        
        <div v-else class="dropdown dropdown-end">
          <label tabindex="0" class="btn btn-ghost btn-circle avatar border-2 border-indigo-100">
            <div class="w-10 rounded-full">
              <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="profile" />
            </div>
          </label>
          <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-3 shadow-xl bg-white rounded-[1.5rem] w-52 border border-slate-100">
            <li class="menu-title text-slate-400 font-bold px-4 py-2">Alberto Lee님 🐜</li>
            <li><router-link to="/profile" class="rounded-xl py-3 px-4 hover:bg-indigo-50 font-medium">내 프로필</router-link></li>
            <li><a @click="authStore.logout" class="rounded-xl py-3 px-4 text-error font-medium hover:bg-error/10">로그아웃</a></li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>