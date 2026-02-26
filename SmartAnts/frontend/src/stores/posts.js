// frontend/src/stores/posts.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
// [수정] user 스토어 import (auth.js 대신 사용)
import { useUserStore } from '@/stores/user' 

export const usePostStore = defineStore('posts', () => {
  const router = useRouter()
  // [수정] user 스토어 사용 설정
  const userStore = useUserStore()
  
  // 1. State (상태)
  const posts = ref([])       // 게시글 목록
  const post = ref(null)      // 게시글 상세 정보
  const loading = ref(false)  // 로딩 상태
  const totalCount = ref(0)   // 페이지네이션용 전체 개수

  // API 기본 URL (설정에 따라 다를 수 있음)
  const API_URL = '/posts'

  // 2. Actions (기능)
  
// [R] 게시글 목록 가져오기
  const getPosts = async (category = null, searchQuery = null, page = 1) => {
    loading.value = true
    try {
      const params = { page }
      if (category) params.category = category
      if (searchQuery) params.search = searchQuery

      const res = await axios.get(`${API_URL}/`, { params })
      
      // ✅ [수정] 데이터 형식 자동 감지 (이게 없어서 에러난 겁니다!)
      if (res.data.results) {
        // 1. 페이지네이션 된 데이터가 왔을 때
        posts.value = res.data.results
        totalCount.value = res.data.count
      } else {
        // 2. 그냥 리스트 데이터가 왔을 때 (현재 백엔드 상태)
        posts.value = res.data
        totalCount.value = res.data.length
      }

    } catch (err) {
      console.error('게시글 목록 조회 실패:', err)
      // 에러 나면 빈 배열로 초기화 (그래야 화면이 안 죽음)
      posts.value = [] 
      totalCount.value = 0
    } finally {
      loading.value = false
    }
  }
      
      // // [변경] 응답 구조에 맞게 데이터 저장
      // posts.value = res.data.results
      // totalCount.value = res.data.count
      // nextPage.value = res.data.next
      // prevPage.value = res.data.previous

      // [수정] 응답 구조 변경 대응
      // 기존: posts.value = res.data
      // 변경: res.data.results가 실제 리스트, res.data.count가 전체 개수
 
  
  // [R] 게시글 상세 조회
  const getPostDetail = async (postId) => {
    loading.value = true
    try {
      const res = await axios.get(`${API_URL}/${postId}/`)
      post.value = res.data
    } catch (err) {
      console.error('게시글 상세 조회 실패:', err)
      // 권한 없음(403)이나 에러 시 뒤로가기
      alert('글을 볼 권한이 없거나 존재하지 않습니다.')
      router.go(-1)
    } finally {
      loading.value = false
    }
  }

  // [C] 게시글 작성
  const createPost = async (payload) => {
    const { title, content, category, is_secret } = payload
    try {
      await axios.post(`${API_URL}/`, {
        title, content, category, is_secret
      }, {
        // [수정] localStorage 직접 접근 -> userStore.token 사용
        // [수정] Token -> Bearer (JWT 표준)
        headers: { Authorization: `Bearer ${userStore.token}` } 
      })
      alert('작성 완료!')
      // 라우터 이름 소문자 'community'로 맞춤 (라우터 설정과 일치해야 함)
      router.push({ name: 'community' }) 
    } catch (err) {
      console.error(err)
      alert('작성 실패!')
    }
  }

  // [Like] 게시글 좋아요
  const likePost = async (postId) => {
    try {
      const res = await axios.post(`${API_URL}/${postId}/like/`, {}, {
        // [수정] Bearer 토큰 적용
        headers: { Authorization: `Bearer ${userStore.token}` }
      })
      // 현재 보고 있는 post 정보 업데이트 (좋아요 수, 하트 상태)
      if (post.value && post.value.id === postId) {
        post.value.like_count = res.data.count
        // 내가 좋아요 눌렀는지 여부도 백엔드에서 주면 좋은데, 
        // 일단 카운트만 갱신하거나 새로고침 필요
      }
      return res.data // { liked: true, count: 10 }
    } catch (err) {
      console.error(err)
      alert('로그인이 필요합니다.')
    }
  }
  
// [U] 게시글 수정 (NEW)
  const updatePost = async (postId, payload) => {
    try {
      const { title, content, category, is_secret } = payload
      await axios.put(`${API_URL}/${postId}/`, {
        title, content, category, is_secret
      }, {
        // [수정] Bearer 토큰 적용
        headers: { Authorization: `Bearer ${userStore.token}` }
      })
      alert('수정이 완료되었습니다.')
      router.push({ name: 'PostDetail', params: { id: postId } }) // 수정 후 상세페이지로
    } catch (err) {
      console.error(err)
      alert('수정 실패! 권한이 없거나 오류가 발생했습니다.')
    }
  }

  // [D] 게시글 삭제 (NEW)
  const deletePost = async (postId) => {
    if (!confirm('정말 이 게시글을 삭제하시겠습니까?')) return

    try {
      await axios.delete(`${API_URL}/${postId}/`, {
        // [수정] Bearer 토큰 적용
        headers: { Authorization: `Bearer ${userStore.token}` }
      })
      alert('삭제되었습니다.')
      // 라우터 이름 소문자 'community'로 맞춤
      router.push({ name: 'community' }) 
    } catch (err) {
      console.error(err)
      alert('삭제 실패! 본인의 글이 아니거나 오류가 발생했습니다.')
    }
  }

  // Return
  return { 
    posts, post, loading, totalCount,
    getPosts, getPostDetail, createPost, likePost, 
    updatePost, deletePost 
  }
})