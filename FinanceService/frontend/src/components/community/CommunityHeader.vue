<template>
  <header class="flex justify-between items-end border-b border-slate-100 pb-8">
    <div>
      <h2 class="text-4xl font-black text-slate-800 tracking-tight">개미 광장 💬</h2>
      <p class="text-slate-400 mt-2 font-medium">똑똑한 개미들의 투자와 금융 이야기</p>
    </div>
    <router-link :to="{ name: 'post-create' }" class="btn btn-primary px-8 rounded-2xl shadow-lg shadow-primary/20">
      글쓰기
    </router-link>
  </header>
</template>