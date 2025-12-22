<template>
  <div class="py-32 text-center bg-white rounded-[3rem] border border-dashed border-slate-200 animate-in fade-in zoom-in duration-500">
    <span class="text-5xl mb-6 block">🐜</span>
    <h3 class="text-xl font-black text-slate-800 mb-2">이 게시판은 아직 조용하네요.</h3>
    <p class="text-slate-400 font-medium">첫 번째 주인공이 되어 지식을 공유해 보세요!</p>
    <router-link :to="{ name: 'post-create' }" class="btn btn-link text-primary font-black mt-4 no-underline">
      글 작성하러 가기 →
    </router-link>
  </div>
</template>