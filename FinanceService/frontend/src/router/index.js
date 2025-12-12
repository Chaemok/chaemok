import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user' 

import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import MapView from '@/views/MapView.vue'
import DepositListView from '@/views/DepositListView.vue'
import MyPageView from '@/views/MyPageView.vue'
import ExchangeView from '@/views/ExchangeView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ProfileEditView from '@/views/ProfileEditView.vue'

import SignUpSucessView from '@/views/SignUpSucessView.vue'
import CommunityView from '@/views/CommunityView.vue'
import PostCreateView from '@/views/PostCreateView.vue'
import PostDetailView from '@/views/PostDetailView.vue'
import PostUpdateView from '@/views/PostUpdateView.vue'

import StockRecommendView from '@/views/StockRecommendView.vue' // 👈 여기서 이미 불러왔음

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },

    { path: '/signup', name: 'signup', component: SignUpView }, 
    { path: '/signup-success', name:'signup-success', component: SignUpSucessView},
    { path: '/login', name: 'login', component: LogInView },
    
    { path: '/mypage', name: 'mypage', component: MyPageView },

    { path: '/community', name: 'community', component: CommunityView },
    { path: '/community/notices', name: 'notices', component: CommunityView }, 
    { path: '/community/posts', name: 'posts', component: CommunityView },     
    { path: '/community/faq', name: 'faq', component: CommunityView },         
    { path: '/community/qna', name: 'qna', component: CommunityView },         

    { path: '/community/create', name: 'PostCreate', component: PostCreateView },
    { path: '/community/:id', name: 'PostDetail', component: PostDetailView },
    { path: '/community/:id/edit', name: 'PostUpdate', component: PostUpdateView },

    { path: '/map', name: 'map', component: MapView },

    { path: '/deposits', name: 'deposits', component: DepositListView },

    { path: '/exchange', name: 'exchange', component: ExchangeView },

    { path: '/profile', name: 'profile', component: ProfileView },
    { path: '/profile/edit', name: 'profile-edit', component: ProfileEditView },
    
    { path: '/stocks/recommend', name: 'stocks-recommend', component: StockRecommendView },
  ]
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  const authRequiredPages = [
    'mypage', 
    'PostCreate', 
    'PostUpdate', 
    'profile', 
    'profile-edit',
    'qna'
  ]

  const isAuthRequired = authRequiredPages.includes(to.name)

  if (isAuthRequired && !userStore.isLogin) {
    alert('로그인이 필요한 서비스입니다.')
    next({ name: 'login' }) 
  } else {
    next() 
  }
})

export default router