<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const store = useUserStore()
const router = useRouter()

const logout = () => {
  store.logOut()
  router.push({ name: 'home' })
}
</script>

<template>
  <div class="dropdown dropdown-end dropdown-hover">
    
    <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar placeholder ring-2 ring-gray-100 hover:ring-blue-200 transition-all">
      <div class="bg-gray-900 text-neutral-content rounded-full w-10">
        <span class="text-lg font-bold text-white">{{ store.username?.charAt(0).toUpperCase() }}</span>
      </div>
    </div>

    <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow-xl bg-white rounded-2xl w-52 border border-gray-100 mt-2">
      <li class="menu-title px-4 py-2">
        <span class="text-gray-900 font-bold text-sm">{{ store.username }}님 안녕하세요! 👋</span>
      </li>
      
      <div class="divider my-0"></div>

      <li>
        <RouterLink :to="{ name: 'mypage' }" class="py-3 font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50">
          👤 마이페이지
        </RouterLink>
      </li>
      <li>
        <RouterLink :to="{ name: 'map' }" class="py-3 font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50">
          ❤️ 찜한 상품
        </RouterLink>
      </li>
      
      <div class="divider my-0"></div>

      <li>
        <button @click="logout" class="py-3 font-medium text-red-500 hover:bg-red-50 hover:text-red-600">
          로그아웃
        </button>
      </li>
    </ul>
  </div>
</template>