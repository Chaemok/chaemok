<template>
  <header class="flex flex-col md:flex-row md:items-end justify-between gap-6 px-4">
    <div class="space-y-2">
      <span class="inline-block px-3 py-1 bg-blue-900 text-white text-[10px] font-black rounded-full tracking-widest uppercase shadow-lg shadow-blue-100">
        Community
      </span>
      <h1 class="text-5xl font-black text-blue-900 tracking-tighter">
        Smart <span class="text-blue-600">Ants</span>
      </h1>
      <p class="text-slate-500 font-bold text-sm">개미들이 서로 토크하는 금융 커뮤니티입니다 🐜</p>
    </div>

    <button @click="$router.push({ name: 'post-create' })" 
      class="flex items-center gap-2 px-8 py-4 bg-blue-600 text-white rounded-2xl font-black shadow-xl shadow-blue-100 hover:bg-blue-700 hover:-translate-y-1 transition-all active:scale-95">
      <span>✏️</span> 새로운 글 작성
    </button>
  </header>
</template>