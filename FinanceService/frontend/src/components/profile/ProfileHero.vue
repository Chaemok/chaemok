<script setup>
defineProps({
  user: Object
})
</script>

<template>
  <div class="bg-primary p-10 text-white rounded-[2.5rem] shadow-xl shadow-primary/20 flex flex-col md:flex-row justify-between items-center gap-6">
    <div class="flex items-center gap-6">
      <div class="avatar">
        <div class="w-24 rounded-3xl ring ring-white ring-offset-base-100 ring-offset-2">
          <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" />
        </div>
      </div>
      <div>
        <h2 class="text-3xl font-black">{{ user?.nickname || '똑똑한 개미' }}님 🐜</h2>
        <p class="text-indigo-100 opacity-80">{{ user?.username }} | SSAFY 14기 주니어 개발자</p>
      </div>
    </div>
    <div class="text-right">
      <p class="text-indigo-100 text-sm mb-1">현재 설정된 연봉</p>
      <p class="text-3xl font-black">{{ (user?.salary || 0).toLocaleString() }}원</p>
    </div>
  </div>
</template>