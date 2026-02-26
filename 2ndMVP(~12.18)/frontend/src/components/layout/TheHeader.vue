<script setup>
import { RouterLink, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import UserDropdown from '@/components/UserDropdown.vue'

const store = useUserStore()
const route = useRoute()

// ✨ 메뉴 구조 개편 (금융 서비스 그룹화)
const menuItems = [
  { 
    name: 'finance', 
    label: '💰 금융 라운지', // 상위 메뉴 이름
    children: [
      { name: 'stocks-recommend', label: '📈 주식 추천' },
      { name: 'deposits', label: '🏦 예/적금 비교' },
      { name: 'exchange', label: '💱 환율 조회' },
      { name: 'map', label: '🗺️ 은행/증권사 지도' }, // 라벨 수정
    ]
  },
  { 
    name: 'community', 
    label: '🗣️ 커뮤니티',
    children: [
      { name: 'notices', label: '📢 공지사항' },
      { name: 'posts', label: '💬 자유게시판' },
      { name: 'faq', label: '❓ FAQ' },
      { name: 'qna', label: '📩 1:1 문의' },
    ]
  },
]
</script>

<template>
  <header class="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200">
    <div class="container mx-auto px-6 h-20 flex items-center justify-between">
      
      <div class="flex items-center gap-4">
        <div class="dropdown lg:hidden">
          <label tabindex="0" class="btn btn-square btn-ghost">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" /></svg>
          </label>
          <ul tabindex="0" class="menu menu-md dropdown-content mt-3 z-[1] p-2 shadow-lg bg-white rounded-box w-52 border border-gray-100">
            <li v-for="item in menuItems" :key="item.name">
              <template v-if="!item.children">
                <RouterLink :to="{ name: item.name }">{{ item.label }}</RouterLink>
              </template>
              <template v-else>
                <details>
                  <summary>{{ item.label }}</summary>
                  <ul>
                    <li v-for="child in item.children" :key="child.name">
                      <RouterLink :to="{ name: child.name }">{{ child.label }}</RouterLink>
                    </li>
                  </ul>
                </details>
              </template>
            </li>
          </ul>
        </div>
        
        <RouterLink :to="{ name: 'home' }" class="flex items-center gap-2 hover:opacity-80 transition-opacity">
          <span class="text-3xl">🐜</span>
           <span class="text-2xl font-extrabold text-gray-900 tracking-tight font-sans">SMART ANTS</span>
        </RouterLink>
      </div>

      <div class="hidden lg:flex items-center gap-8">
        <template v-for="item in menuItems" :key="item.name">
          
          <div class="dropdown dropdown-hover group">
            <div 
              role="button" 
              tabindex="0"
              class="text-[17px] font-semibold text-gray-500 group-hover:text-blue-600 transition-colors py-6 inline-flex items-center gap-1 outline-none cursor-pointer"
              :class="{ 'text-blue-600 font-bold': route.path?.includes(item.name) }"
            >
              {{ item.label }}
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3 h-3 transition-transform duration-300 group-hover:rotate-180">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
              </svg>
            </div>

            <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow-xl bg-white rounded-2xl w-56 border border-gray-100 mt-0">
              <li v-for="child in item.children" :key="child.name">
                <RouterLink 
                  :to="{ name: child.name }" 
                  class="font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50 py-3"
                  active-class="text-blue-600 bg-blue-50 font-bold"
                >
                  {{ child.label }}
                </RouterLink>
              </li>
            </ul>
          </div>

        </template>
      </div>

      <div class="flex items-center gap-3">
        <template v-if="!store.isLogin">
          <RouterLink :to="{ name: 'login' }" class="btn btn-ghost text-base font-medium">로그인</RouterLink>
          <RouterLink :to="{ name: 'signup' }" class="btn bg-gray-900 text-white hover:bg-gray-800 border-none px-6 text-base rounded-full">회원가입</RouterLink>
        </template>
        <template v-else>
          <UserDropdown />
        </template>
      </div>

    </div>
  </header>
</template>