<template>
  <section class="relative bg-gradient-to-br from-indigo-600 via-indigo-700 to-slate-900 rounded-[3rem] overflow-hidden text-white p-12 md:p-20 shadow-2xl">
    <div class="relative z-10 space-y-8 max-w-3xl">
      <div class="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-md rounded-full text-indigo-100 text-sm font-bold border border-white/20">
        <span class="animate-pulse">✨</span> 신규: AI 주식 랭킹 업데이트 🐜
      </div>
      
      <h1 class="text-5xl md:text-6xl font-black leading-[1.15] tracking-tight">
        채목님의 연봉에 딱 맞는<br />
        <span class="text-indigo-300">금융 전략</span>을 세워보세요.
      </h1>
      
      <p class="text-lg md:text-xl text-indigo-100/80 font-medium leading-relaxed">
        전국 은행 예적금부터 퀀트 기반 주식 추천까지,<br />
        스마트한 개미들의 투자 놀이터입니다.
      </p>

      <div class="flex flex-wrap gap-4 pt-4">
        <button @click="$router.push('/profile')" class="px-8 py-4 bg-white text-indigo-700 font-black rounded-2xl hover:bg-indigo-50 transition-all shadow-lg hover:shadow-indigo-500/20">
          내 자산 분석하기
        </button>
        <button @click="$router.push('/deposit')" class="px-8 py-4 bg-indigo-500/30 backdrop-blur-md border border-white/30 text-white font-black rounded-2xl hover:bg-white/10 transition-all">
          상품 둘러보기
        </button>
      </div>
    </div>

    <div class="absolute bottom-[-10%] right-[-5%] text-[20rem] font-black text-white/[0.03] select-none pointer-events-none italic">
      ANTS
    </div>
  </section>
</template>