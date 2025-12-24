<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import UserAvatar from '@/components/auth/UserAvatar.vue'

const authStore = useAuthStore()
const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)

const mainMenus = [
  { 
    name: '금융 상품', path: '/deposit', 
    sub: [{ name: '예/적금 상품', path: '/deposit' }, { name: '주식 종목 추천', path: '/stocks' }]
  },
  { 
    name: '시장 지표', path: '/market', 
    sub: [{ name: '시장 대시보드', path: '/market' }, { name: '오늘의 환율', path: '/market/exchange-rate' }, { name: '금/은 시세', path: '/market/commodity' }]
  },
  { 
    name: '커뮤니티', path: '/community', 
    sub: [
      { name: '자유게시판', path: '/community', query: { category: 'free' } },
      { name: 'Q&A', path: '/community', query: { category: 'qna' } },
      { name: '상품후기', path: '/community', query: { category: 'review' } },
      { name: '투자꿀팁', path: '/community', query: { category: 'tips' } }, // tips로 수정 (중복 방지)
      { name: 'FAQ', path: '/community', query: { category: 'faq' } },
      { name: '1:1 문의', path: '/community', query: { category: 'inquiry' } }
    ]
  },
  { name: '금융 뉴스', path: '/news' },
  { name: 'YouTube', path: '/youtube', isSpecial: true },
]

const handleScroll = () => { isScrolled.value = window.scrollY > 10 }
const toggleMobileMenu = () => { isMobileMenuOpen.value = !isMobileMenuOpen.value }

onMounted(() => window.addEventListener('scroll', handleScroll))
onUnmounted(() => window.removeEventListener('scroll', handleScroll))
</script>

<template>
  <nav class="fixed top-0 left-0 w-full z-[100] transition-all duration-300 shadow-sm font-pretendard">
    
    <div class="h-11 bg-slate-900 flex items-center border-b border-white/5">
      <div class="max-w-7xl mx-auto w-full px-6 flex justify-between items-center">
        <p class="hidden sm:block text-[11px] font-black text-slate-500 tracking-[0.2em] uppercase">
          Smart Ants Financial Intelligence
        </p>
        <div class="flex items-center gap-6 text-xs font-bold">
          <router-link to="/map" class="text-slate-300 hover:text-white transition-colors">은행 찾기</router-link>
          <div v-if="!authStore.isLoggedIn" class="flex gap-5 border-l border-slate-700 pl-6">
            <router-link to="/login" class="text-slate-300 hover:text-white">로그인</router-link>
            <router-link to="/signup" class="text-blue-400 hover:text-blue-300 font-black tracking-tight">회원가입</router-link>
          </div>
          <button v-else @click="authStore.logout" class="text-rose-400 hover:text-rose-300 ml-6">로그아웃</button>
        </div>
      </div>
    </div>

    <div 
      class="w-full bg-white/95 backdrop-blur-md transition-all duration-300 border-b border-slate-200"
      :class="[isScrolled ? 'h-16' : 'h-20']"
    >
      <div class="max-w-7xl mx-auto h-full px-6 flex items-center justify-between">
        
        <router-link to="/" class="flex items-center gap-2 group" @click="isMobileMenuOpen = false">
          <span class="text-2xl transition-transform group-hover:scale-110">🐜</span>
          <span class="text-xl font-black tracking-tighter">
            <span class="text-[#1e3a8a]">Smart</span><span class="text-[#2563eb]">Ants</span>
          </span>
        </router-link>

        <div class="hidden lg:flex items-center gap-1 h-full">
          <div v-for="link in mainMenus" :key="link.path" class="relative h-full group/menu">
            <router-link 
              :to="link.path"
              class="px-5 h-full flex items-center text-[15px] font-bold text-slate-600 hover:text-blue-600 transition-all relative"
              active-class="!text-blue-600"
            >
              {{ link.name }}
              <div v-if="$route.path.startsWith(link.path)" class="absolute bottom-0 left-0 w-full h-1 bg-blue-600 rounded-t-full"></div>
            </router-link>

            <div v-if="link.sub" 
                 class="absolute top-[calc(100%-5px)] left-0 min-w-[190px] bg-white border border-slate-100 shadow-2xl rounded-2xl p-3 opacity-0 translate-y-4 pointer-events-none group-hover/menu:opacity-100 group-hover/menu:translate-y-0 group-hover/menu:pointer-events-auto transition-all duration-300 ease-out">
              <router-link 
                v-for="sub in link.sub" 
                :key="sub.name" 
                :to="{ path: sub.path, query: sub.query }" 
                class="block px-4 py-3 text-[13px] font-bold text-slate-500 hover:bg-blue-50 hover:text-blue-600 rounded-xl transition-colors"
              >
                {{ sub.name }}
              </router-link>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-4">
          <router-link v-if="authStore.isLoggedIn" to="/user/mypage" class="flex items-center gap-3">
            <div class="hidden md:block text-right">
              <p class="text-[9px] font-black text-slate-400 leading-none mb-1 uppercase">My Ants</p>
              <p class="text-xs font-bold text-slate-800">{{ authStore.user?.nickname }}님</p>
            </div>
            <UserAvatar :image="authStore.user?.profile_image" :name="authStore.user?.nickname" sizeClass="w-9 h-9 border border-slate-200" />
          </router-link>

          <button @click="toggleMobileMenu" class="lg:hidden p-2 text-slate-600 hover:bg-slate-100 rounded-xl transition-colors">
            <svg v-if="!isMobileMenuOpen" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-7 h-7">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 9h16.5m-16.5 6.75h16.5" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-7 h-7">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="translate-x-full"
      enter-to-class="translate-x-0"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="translate-x-0"
      leave-to-class="translate-x-full"
    >
      <div v-if="isMobileMenuOpen" class="fixed inset-0 top-[124px] bg-white z-[90] lg:hidden overflow-y-auto px-6 py-8 border-t border-slate-100">
        <div class="space-y-8 pb-20">
          <div v-for="link in mainMenus" :key="link.path" class="space-y-4">
            <p class="text-xs font-black text-slate-400 uppercase tracking-widest pl-2">{{ link.name }}</p>
            <div class="flex flex-col gap-1">
              <router-link 
                v-if="!link.sub" :to="link.path" @click="isMobileMenuOpen = false"
                class="p-4 bg-slate-50 rounded-2xl text-lg font-black text-slate-800"
              >
                {{ link.name }}
              </router-link>
              <template v-else>
                <router-link 
                  v-for="sub in link.sub" 
                  :key="sub.name" 
                  :to="{ path: sub.path, query: sub.query }" 
                  @click="isMobileMenuOpen = false"
                  class="p-4 hover:bg-blue-50 rounded-2xl text-[17px] font-bold text-slate-700 flex justify-between items-center"
                >
                  {{ sub.name }}
                  <span class="text-slate-300 text-xl">›</span>
                </router-link>
              </template>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </nav>
</template>

<style scoped>
.group-hover\/menu\:opacity-100 { transition-delay: 50ms; }
.group\/menu:hover .group-hover\/menu\:opacity-100 { opacity: 1; transform: translateY(0); pointer-events: auto; }
.mobile-menu-enter-active, .mobile-menu-leave-active { transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
.mobile-menu-enter-from, .mobile-menu-leave-to { transform: translateX(100%); }
.font-pretendard { font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif; }
</style>