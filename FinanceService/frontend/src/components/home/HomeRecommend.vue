<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

defineProps({
  products: { type: Array, default: () => [] }
})
</script>

<template>
  <section v-if="userStore.isLogin && products.length > 0" class="bg-black text-white py-20 mb-24">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex flex-col md:flex-row justify-between items-end mb-10">
        <div>
          <span class="text-blue-400 font-bold tracking-widest uppercase">For You</span>
          <h2 class="text-4xl font-bold mt-2">{{ userStore.username }}님을 위한 <br>맞춤 포트폴리오</h2>
        </div>
        <button @click="router.push({name: 'deposits'})" class="text-gray-400 hover:text-white underline mt-4 md:mt-0">더보기</button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="product in products" :key="product.id"
             class="bg-gray-800 p-8 rounded-3xl hover:bg-gray-700 transition-colors cursor-pointer group"
             @click="router.push({name: 'deposit-detail', params: {id: product.id}})">
          <div class="flex justify-between items-start mb-6">
             <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full">RECOMMEND</span>
             <span class="text-gray-400 text-sm group-hover:text-white">{{ product.bank_name }}</span>
          </div>
          <h3 class="text-xl font-bold mb-2 line-clamp-2 h-14">{{ product.product_name }}</h3>
          <div class="flex items-end gap-2">
            <span class="text-3xl font-bold text-blue-400">{{ product.highest_rate }}%</span>
            <span class="text-sm text-gray-400 mb-1">최고 금리</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>