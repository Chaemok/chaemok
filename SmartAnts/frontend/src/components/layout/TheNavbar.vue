<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import UserAvatar from '@/components/auth/UserAvatar.vue'

const authStore = useAuthStore()
const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)

const mainMenus = [
  { 
    name: '금융 소식', path: '/news', 
    sub: [
      { name: '금융 뉴스', path: '/news' },
      { name: '금융 YouTube', path: '/youtube', isSpecial: true },
    ]
  },
  { 
    name: '금융 상품', path: '/deposit', 
    sub: [{ name: '예/적금 상품', path: '/deposit' }]
    // { name: '주식 종목 추천', path: '/stocks' }]
  },
  { 
    name: '금융 시장 지표', path: '/market', 
    sub: [{ name: '주식 시장 대시보드', path: '/market' }, { name: '환율 정보', path: '/market/exchange-rate' }, { name: '금/은 시세', path: '/market/commodity' }]
  },
  { 
    name: '커뮤니티', path: '/community', 
    sub: [
      { name: '자유게시판', path: '/community', query: { category: 'free' } },
      { name: 'Q&A', path: '/community', query: { category: 'qna' } },
      { name: '상품후기', path: '/community', query: { category: 'review' } },
      { name: '투자꿀팁', path: '/community', query: { category: 'tips' } },
      { name: 'FAQ', path: '/community', query: { category: 'faq' } },
      { name: '1:1 문의', path: '/community', query: { category: 'inquiry' } }
    ]
  },
]

const handleScroll = () => { isScrolled.value = window.scrollY > 10 }
const toggleMobileMenu = () => { isMobileMenuOpen.value = !isMobileMenuOpen.value }

// 모바일 메뉴 열렸을 때 스크롤 막기
const preventScroll = (isOpen) => {
  document.body.style.overflow = isOpen ? 'hidden' : ''
}

onMounted(() => window.addEventListener('scroll', handleScroll))
onUnmounted(() => window.removeEventListener('scroll', handleScroll))
</script>

<template>
  <nav class="fixed top-0 left-0 w-full z-[100] font-pretendard">
    
    <div class="hidden md:block bg-slate-950 text-white transition-all duration-300 overflow-hidden"
         :class="[isScrolled ? 'h-0' : 'h-10']">
      <div class="max-w-7xl mx-auto w-full px-6 h-full flex justify-between items-center">
        <p class="text-[10px] font-bold text-slate-400 tracking-[0.15em] uppercase">
          Smart Ants Financial Intelligence
        </p>
        
        <div class="flex items-center gap-5 text-[11px] font-medium text-slate-300">
          <div class="flex items-center gap-3">
            <router-link to="/map" class="hover:text-white transition-colors flex items-center gap-1">은행/증권사 찾기</router-link>
            <span class="w-[1px] h-2.5 bg-slate-700"></span>
            <router-link :to="{ path: '/community', query: { category: 'faq' } }" class="hover:text-white transition-colors">자주 묻는 질문</router-link>
            <span class="w-[1px] h-2.5 bg-slate-700"></span>
            <router-link :to="{ path: '/community', query: { category: 'inquiry' } }" class="hover:text-white transition-colors">1:1 문의</router-link>

            
          </div>

          <div v-if="!authStore.isLoggedIn" class="flex gap-4 border-l border-slate-700 pl-5 ml-2">
            <router-link to="/login" class="hover:text-white">로그인</router-link>
            <router-link to="/signup" class="text-blue-400 hover:text-blue-300 font-bold">회원가입</router-link>
          </div>
          <button v-else @click="authStore.logout" class="text-rose-400 hover:text-rose-300 ml-6 font-bold">로그아웃</button>
        </div>
      </div>
    </div>

    <div 
      class="w-full bg-white/90 backdrop-blur-md border-b border-slate-200/60 transition-all duration-500 ease-in-out"
      :class="[isScrolled ? 'h-16 shadow-lg shadow-slate-200/40' : 'h-20']"
    >
      <div class="max-w-7xl mx-auto h-full px-6 flex items-center justify-between">
        
        <router-link to="/" class="flex items-center gap-2 group relative z-[110]" @click="isMobileMenuOpen = false">
          <div class="w-8 h-8 bg-slate-900 rounded-lg flex items-center justify-center group-hover:bg-blue-600 transition-colors duration-300 shadow-lg shadow-slate-300/50">
            <span class="text-lg group-hover:scale-110 transition-transform">🐜</span>
          </div>
          <span class="text-xl font-black tracking-tighter text-slate-900">
            Smart<span class="text-blue-600">Ants</span>
          </span>
        </router-link>

        <div class="hidden md:flex items-center gap-2 h-full">
          <div v-for="link in mainMenus" :key="link.path" class="relative h-full flex items-center group/menu px-1">
            <router-link 
              :to="link.path"
              class="px-4 py-2 rounded-full text-[15px] font-bold text-slate-600 hover:text-blue-600 hover:bg-blue-50 transition-all relative"
              active-class="!text-blue-600 bg-blue-50"
            >
              {{ link.name }}
            </router-link>
            <div v-if="link.sub" class="absolute top-[80%] left-1/2 -translate-x-1/2 min-w-[180px] bg-white border border-slate-100 shadow-xl rounded-2xl p-2 opacity-0 translate-y-4 pointer-events-none group-hover/menu:opacity-100 group-hover/menu:translate-y-0 group-hover/menu:pointer-events-auto transition-all duration-300 ease-out z-50">
               <div class="absolute -top-2 left-1/2 -translate-x-1/2 w-3 h-3 bg-white border-t border-l border-slate-100 rotate-45"></div>
               <router-link v-for="sub in link.sub" :key="sub.name" :to="{ path: sub.path, query: sub.query }" class="block px-4 py-2.5 text-[13px] font-bold text-slate-500 hover:bg-slate-50 hover:text-blue-600 rounded-xl transition-colors text-center">
                 {{ sub.name }}
               </router-link>
            </div>
          </div>
        </div>

        <div class="hidden md:flex items-center gap-4">
          <router-link v-if="authStore.isLoggedIn" to="/user/mypage" class="flex items-center gap-3 pl-4 border-l border-slate-100">
            <div class="text-right">
              <p class="text-[9px] font-black text-slate-400 leading-none mb-1 uppercase tracking-wider">Welcome</p>
              <p class="text-xs font-bold text-slate-900">{{ authStore.user?.nickname || '회원' }}님</p>
            </div>
            <UserAvatar :image="authStore.user?.profile_image" :name="authStore.user?.nickname" sizeClass="w-9 h-9 border-2 border-white shadow-md shadow-slate-200" />
          </router-link>
        </div>

        <button @click="toggleMobileMenu" class="md:hidden p-2 text-slate-800 hover:bg-slate-100 rounded-xl transition-colors relative z-[110]">
          <svg v-if="!isMobileMenuOpen" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-7 h-7">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 9h16.5m-16.5 6.75h16.5" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-7 h-7 text-slate-900">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <transition name="fade">
      <div v-if="isMobileMenuOpen" @click="toggleMobileMenu" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] md:hidden"></div>
    </transition>

    <transition name="slide-right">
      <div v-if="isMobileMenuOpen" class="fixed top-0 right-0 h-full w-[300px] max-w-[85vw] bg-white z-[105] shadow-2xl p-6 overflow-y-auto md:hidden flex flex-col">
        
        <div class="mt-16 mb-8 pb-8 border-b border-slate-100">
          <div v-if="!authStore.isLoggedIn" class="space-y-3">
            <h3 class="text-xl font-black text-slate-900 mb-2">로그인이 필요합니다.</h3>
            <div class="grid grid-cols-2 gap-3">
              <router-link to="/login" @click="toggleMobileMenu" class="py-3 text-center bg-slate-900 text-white rounded-xl font-bold text-sm">로그인</router-link>
              <router-link to="/signup" @click="toggleMobileMenu" class="py-3 text-center bg-blue-50 text-blue-600 rounded-xl font-bold text-sm">회원가입</router-link>
            </div>
          </div>
          <div v-else class="flex items-center gap-4">
            <UserAvatar :image="authStore.user?.profile_image" :name="authStore.user?.nickname" sizeClass="w-12 h-12" />
            <div>
              <p class="text-xs text-slate-400 font-bold uppercase">Welcome Back!</p>
              <p class="text-lg font-black text-slate-900">{{ authStore.user?.nickname }}님</p>
            </div>
            <button @click="authStore.logout" class="ml-auto text-xs text-slate-400 underline">로그아웃</button>
          </div>
        </div>

        <div class="flex-1 space-y-6">
          <div v-for="link in mainMenus" :key="link.path" class="space-y-3">
            <p class="text-xs font-black text-slate-400 uppercase tracking-widest pl-1">{{ link.name }}</p>
            <div class="space-y-1">
              <template v-if="link.sub">
                <router-link v-for="sub in link.sub" :key="sub.name" :to="{ path: sub.path, query: sub.query }" 
                   @click="toggleMobileMenu"
                   class="block p-3 hover:bg-slate-50 rounded-xl text-slate-600 font-bold text-sm transition-colors flex justify-between">
                  {{ sub.name }}
                  <span class="text-slate-300">›</span>
                </router-link>
              </template>
            </div>
          </div>
        </div>

        <div class="mt-8 pt-6 border-t border-slate-100 grid grid-cols-3 gap-2 text-[11px] font-bold text-slate-500 text-center">
          <router-link :to="{ path: '/community', query: { category: 'faq' } }" @click="toggleMobileMenu" class="p-2 bg-slate-50 rounded-lg">FAQ</router-link>
          <router-link :to="{ path: '/community', query: { category: 'inquiry' } }" @click="toggleMobileMenu" class="p-2 bg-slate-50 rounded-lg">1:1문의</router-link>
          <router-link to="/map" @click="toggleMobileMenu" class="p-2 bg-slate-50 rounded-lg">지점찾기</router-link>
        </div>
      </div>
    </transition>
  </nav>
</template>

<style scoped>
.font-pretendard { font-family: 'Pretendard', sans-serif; }

/* 오버레이 페이드 효과 */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* 오른쪽 슬라이드 효과 */
.slide-right-enter-active, .slide-right-leave-active { transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-right-enter-from, .slide-right-leave-to { transform: translateX(100%); }
</style>