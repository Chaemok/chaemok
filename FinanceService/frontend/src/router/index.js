import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/Home/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  // 🐜 [추가] 페이지 이동 시 항상 스크롤을 맨 위로 올려주는 기본 디테일
  scrollBehavior() {
    return { top: 0 }
  },
  routes: [
    { path: '/', name: 'home', component: HomeView },
    
    // [Auth]
    { path: '/login', name: 'login', component: () => import('@/views/Auth/LoginView.vue') },
    { path: '/signup', name: 'signup', component: () => import('@/views/Auth/SignupView.vue') },

    // [Finance]
    { path: '/deposit', name: 'deposit', component: () => import('@/views/Finance/DepositListView.vue') },
    { path: '/exchange', name: 'exchange', component: () => import('@/views/Finance/ExchangeView.vue') },
    { path: '/stocks', name: 'stock-recommendation', component: () => import('@/views/Finance/StockRecommendationView.vue') },

    
    // [Map]
    { path: '/map', name: 'map', component: () => import('@/views/Map/MapView.vue') },

    // [User]
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/User/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile/edit',
      name: 'profile-edit',
      component: () => import('@/views/User/ProfileEditView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile/password',
      name: 'password-change',
      component: () => import('@/views/User/PasswordChangeView.vue'),
      meta: { requiresAuth: true }
    },

    // [Community]
    {
      path: '/community',
      name: 'community',
      component: () => import('@/views/Community/CommunityView.vue')
    },
    {
      path: '/community/create',
      name: 'post-create',
      component: () => import('@/views/Community/PostCreateView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/community/:id',
      name: 'post-detail',
      component: () => import('@/views/Community/PostDetailView.vue'),
    }
  ]
})

// 🐜 네비게이션 가드 최적화
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 인증이 필요한 페이지인데 로그인이 안 된 경우
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    alert('로그인이 필요한 서비스입니다 🐜')
    next({ name: 'login' })
  } 
  // 이미 로그인했는데 로그인/회원가입 페이지로 가려는 경우 (선택 사항)
  else if ((to.name === 'login' || to.name === 'signup') && authStore.isLoggedIn) {
    next({ name: 'home' })
  }
  // 그 외 모든 경우는 정상 이동
  else {
    next()
  }
})

export default router