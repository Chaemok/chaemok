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

    // 📈 [Market] 금융 지표 및 주식 정보 허브
    { 
      path: '/market', 
      component: () => import('@/views/Market/MarketLayout.vue'),
      children: [
        { path: '', name: 'market-overview', component: () => import('@/views/Market/MarketOverView.vue') },
        { path: 'exchange-rate', name: 'market-exchange', component: () => import('@/views/Finance/ExchangeView.vue') },
        { path: 'commodity', name: 'market-commodity', component: () => import('@/views/Finance/SpotProductView.vue') },
        { path: 'stock/:code', name: 'stock-detail', component: () => import('@/views/Market/StockDetailView.vue') },
      ]
    },

    // 💬 [Community] 소통 및 게시판 계층화
    {
      path: '/community',
      component: () => import('@/views/Community/CommunityLayout.vue'),
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

    // 👤 [User] 마이페이지 및 프로필 계층화
    {
      path: '/user',
      meta: { requiresAuth: true }, // 전체 하위 경로에 인증 필요 설정 가능
      children: [
        { path: 'mypage', name: 'mypage', component: () => import('@/views/User/MyPageView.vue') },
        { path: 'profile', name: 'profile-detail', component: () => import('@/views/User/ProfileView.vue') },
        { path: 'profile/edit', name: 'profile-edit', component: () => import('@/views/User/ProfileEditView.vue') },
        { path: 'password', name: 'password-change', component: () => import('@/views/User/PasswordChangeView.vue') }
      ]
    },

    // [Finance/News/Map] 나머지 독립 경로
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
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  if (requiresAuth && !authStore.isLoggedIn) {
    alert('로그인이 필요한 서비스입니다 🐜')
    next({ name: 'login' })
  } 
  else if ((to.name === 'login' || to.name === 'signup') && authStore.isLoggedIn) {
    next({ name: 'home' })
  }
  else {
    next()
  }
})

export default router