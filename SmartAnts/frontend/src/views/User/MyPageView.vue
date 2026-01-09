<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useFinanceStore } from '@/stores/finance' // 🐜 스토어 추가
import { useRouter } from 'vue-router'
import api from '@/api' 
import ProfileHero from '@/components/profile/ProfileHero.vue'
import JoinedProducts from '@/components/profile/JoinedProducts.vue'

const authStore = useAuthStore()
const financeStore = useFinanceStore() // 🐜 Finance 스토어 사용
const router = useRouter()

const activeTab = ref('joined') // joined | activity | likes
const isLoading = ref(true)

// 게시글/댓글 데이터
const myPosts = ref([])
const myComments = ref([])

// 🐜 가입한 상품은 스토어의 상태(State)를 바로 바라보게 합니다. (반응형 유지)
const depositList = computed(() => financeStore.joined.deposits)
const savingList = computed(() => financeStore.joined.savings)

const fetchMyData = async () => {
  isLoading.value = true
  
  try {
    // 1. 🐜 가입 상품 목록 로드 (백엔드 accounts/serializers 수정 덕분에 여기서 한방에 해결)
    await financeStore.fetchJoinedProducts()

    // 2. 내 게시글/댓글 (Community 기능이 있다면 유지)
    try {
      // (혹시 Community API가 준비 안 되었다면 에러 날 수 있으니 try-catch)
      const postRes = await api.get('community/posts/mine/') 
      myPosts.value = postRes.data
    } catch (e) { 
        // console.log('게시글 로드 패스') 
    }

    try {
      const commentRes = await api.get('community/comments/mine/')
      myComments.value = commentRes.data
    } catch (e) { 
        // console.log('댓글 로드 패스') 
    }

  } catch (err) {
    console.error('마이페이지 데이터 로드 실패', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchMyData()
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 pb-20">
    <ProfileHero :user="authStore.user" />

    <main class="max-w-4xl mx-auto px-4 -mt-10 relative z-10">
      
      <div class="bg-white rounded-2xl shadow-sm p-2 flex mb-8">
        <button 
          v-for="tab in [
            { id: 'joined', label: '가입 상품', icon: '🏦' },
            { id: 'activity', label: '내 활동', icon: '📝' },
            { id: 'likes', label: '관심 목록', icon: '❤️' }
          ]"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="flex-1 py-3 rounded-xl text-sm font-bold transition-all flex items-center justify-center gap-2"
          :class="activeTab === tab.id ? 'bg-slate-900 text-white shadow-md' : 'text-slate-400 hover:bg-slate-50'"
        >
          <span>{{ tab.icon }}</span>
          {{ tab.label }}
        </button>
      </div>

      <div class="min-h-[300px]">
        
        <div v-if="activeTab === 'joined'" class="space-y-10 animate-in fade-in slide-in-from-bottom-4 duration-500">
           <JoinedProducts type="예금" :products="depositList" />
           <hr class="border-slate-100">
           <JoinedProducts type="적금" :products="savingList" />
        </div>

        <div v-if="activeTab === 'activity'" class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div class="space-y-4">
              <h3 class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                <span>📄</span> 내가 쓴 글 <span class="text-slate-400 text-sm">({{ myPosts.length }})</span>
              </h3>
              <div v-if="myPosts.length > 0" class="grid gap-3">
                <div v-for="post in myPosts" :key="post.id"
                     @click="router.push(`/community/${post.id}`)" 
                     class="p-5 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all cursor-pointer">
                  <h4 class="font-bold text-slate-800 mb-1">{{ post.title }}</h4>
                  <p class="text-xs text-slate-400">{{ post.created_at?.slice(0,10) }} 작성</p>
                </div>
              </div>
              <p v-else class="text-center py-8 bg-slate-50/50 rounded-2xl text-slate-400 text-sm">작성한 게시글이 없습니다.</p>
            </div>

            <div class="space-y-4">
              <h3 class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                <span>💬</span> 내가 쓴 댓글 <span class="text-slate-400 text-sm">({{ myComments.length }})</span>
              </h3>
              <div v-if="myComments.length > 0" class="grid gap-3">
                <div v-for="comment in myComments" :key="comment.id"
                     @click="router.push(`/community/${comment.article}`)" 
                     class="p-5 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all cursor-pointer">
                  <p class="font-medium text-slate-700 text-sm truncate mb-1">"{{ comment.content }}"</p>
                  <p class="text-xs text-slate-400">{{ comment.created_at?.slice(0,10) }} 작성</p>
                </div>
              </div>
              <p v-else class="text-center py-8 bg-slate-50/50 rounded-2xl text-slate-400 text-sm">작성한 댓글이 없습니다.</p>
            </div>
        </div>

        <div v-if="activeTab === 'likes'" class="flex flex-col items-center justify-center py-20 animate-in fade-in">
             <span class="text-6xl mb-6 grayscale opacity-30">❤️</span>
             <h3 class="text-lg font-bold text-slate-800 mb-2">관심 목록</h3>
             <p class="text-slate-400 font-medium text-sm">찜한 게시글이나 상품이 이곳에 표시됩니다.</p>
        </div>

      </div>
    </main>
  </div>
</template>