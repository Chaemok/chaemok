<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <section class="max-w-7xl mx-auto px-6 mb-24">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div @click="router.push({name: 'deposits'})" class="group bg-gray-50 hover:bg-blue-600 hover:text-white p-8 rounded-3xl cursor-pointer transition-all duration-300">
        <div class="text-4xl mb-4 group-hover:scale-110 transition-transform">💰</div>
        <h3 class="text-xl font-bold mb-1">예/적금 상품 조회</h3>
        <p class="text-sm text-gray-500 group-hover:text-blue-100">최고 금리 비교</p>
      </div>
      <div @click="router.push({name: 'exchange'})" class="group bg-gray-50 hover:bg-blue-600 hover:text-white p-8 rounded-3xl cursor-pointer transition-all duration-300">
        <div class="text-4xl mb-4 group-hover:scale-110 transition-transform">💱</div>
        <h3 class="text-xl font-bold mb-1">환율 계산</h3>
        <p class="text-sm text-gray-500 group-hover:text-blue-100">실시간 환율 정보</p>
      </div>
      <div @click="router.push({name: 'map'})" class="group bg-gray-50 hover:bg-blue-600 hover:text-white p-8 rounded-3xl cursor-pointer transition-all duration-300">
        <div class="text-4xl mb-4 group-hover:scale-110 transition-transform">🗺️</div>
        <h3 class="text-xl font-bold mb-1">은행 지도</h3>
        <p class="text-sm text-gray-500 group-hover:text-blue-100">내 주변 은행 찾기</p>
      </div>
      <div @click="router.push({name: 'posts'})" class="group bg-gray-50 hover:bg-blue-600 hover:text-white p-8 rounded-3xl cursor-pointer transition-all duration-300">
        <div class="text-4xl mb-4 group-hover:scale-110 transition-transform">🗣️</div>
        <h3 class="text-xl font-bold mb-1">커뮤니티</h3>
        <p class="text-sm text-gray-500 group-hover:text-blue-100">금융 꿀팁 공유</p>
      </div>
    </div>
  </section>
</template>