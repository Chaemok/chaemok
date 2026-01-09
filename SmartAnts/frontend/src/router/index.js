import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/Home/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior() {
    return { top: 0 }
  },
  routes: [
    { path: '/', name: 'home', component: HomeView },
    
    // 🐜 [Auth]
    { path: '/login', name: 'login', component: () => import('@/views/Auth/LoginView.vue') },
    { path: '/signup', name: 'signup', component: () => import('@/views/Auth/SignupView.vue') },

    // 📈 [Market]
    { 
      path: '/market', 
      component: () => import('@/components/layout/MarketLayout.vue'),
      children: [
        { path: '', name: 'market-overview', component: () => import('@/views/Market/MarketOverView.vue') },
        { path: 'exchange-rate', name: 'market-exchange', component: () => import('@/views/Market/ExchangeView.vue') },
        { path: 'commodity', name: 'market-commodity', component: () => import('@/views/Market/SpotProductView.vue') },
        { path: 'stock/:code', name: 'stock-detail', component: () => import('@/views/Market/StockDetailView.vue') },
      ]
    },

    // 💬 [Community]
    {
      path: '/community',
      component: () => import('@/components/community/CommunityLayout.vue'),
      children: [
        { path: '', name: 'community', component: () => import('@/views/Community/CommunityView.vue') },
        { 
          path: 'create', 
          name: 'post-create', 
          component: () => import('@/views/Community/PostCreateView.vue'), 
          meta: { requiresAuth: true } 
        },
        { path: ':id', name: 'post-detail', component: () => import('@/views/Community/PostDetailView.vue') },
        { 
          path: ':id/edit', 
          name: 'post-edit', 
          component: () => import('@/views/Community/PostEditView.vue'), 
          meta: { requiresAuth: true } 
        }
      ]
    },

    // 👤 [User]
    {
      path: '/user',
      meta: { requiresAuth: true }, 
      children: [
        { path: 'mypage', name: 'mypage', component: () => import('@/views/User/MyPageView.vue') },
        { path: 'profile', name: 'profile-detail', component: () => import('@/views/User/ProfileView.vue') },
        { path: 'profile/edit', name: 'profile-edit', component: () => import('@/views/User/ProfileEditView.vue') },
        { path: 'password', name: 'password-change', component: () => import('@/views/User/PasswordChangeView.vue') },
        { path: 'profile', name: 'profile-detail', component: () => import('@/views/User/PrivateInfoView.vue') },
      ]
    },
    
    // 🤖 [AI BOT] - 에러 수정 완료 (중복 component 제거)
    { 
      path: '/aibot', 
      name: 'aibot', 
      // 만약 파일을 'views/AiBot/AiBotView.vue' 폴더 안에 만들었다면 경로를 수정하세요!
      // 현재는 'views/AiBotView.vue' 기준입니다.
      component: () => import('@/views/AiBotView.vue'), 
      meta: { requiresAuth: true } 
    }, 

    // [Finance/News/Map]
    { path: '/deposit', name: 'deposit', component: () => import('@/views/Finance/DepositListView.vue') },
    { path: '/news', name: 'news', component: () => import('@/views/News/NewsView.vue') },
    { path: '/map', name: 'map', component: () => import('@/views/Map/MapView.vue') },
    { path: '/youtube', name: 'youtube', component: () => import('@/views/Finance/YoutubeView.vue') },
    { path: '/stocks', name: 'stock-recommendation', component: () => import('@/views/Finance/StockRecommendationView.vue') }
  ]
})

// 🐜 네비게이션 가드 최적화
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 인증이 필요한지 확인
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  // 🚨 [수정 중요] isLoggedIn -> isAuthenticated (스토어 변수명과 일치시켜야 함)
  if (requiresAuth && !authStore.isAuthenticated) {
    alert('로그인이 필요한 서비스입니다 🐜')
    next({ name: 'login' })
  } 
  // 로그인 상태에서 로그인/회원가입 페이지 접근 시 홈으로 리다이렉트
  else if ((to.name === 'login' || to.name === 'signup') && authStore.isAuthenticated) {
    next({ name: 'home' })
  }
  else {
    next()
  }
})

export default router