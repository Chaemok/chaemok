<template>
  <section>
    <div class="bg-slate-900 rounded-[3rem] p-12 md:p-16 text-center text-white relative overflow-hidden group">
      <div class="absolute inset-0 bg-[linear-gradient(45deg,transparent_25%,rgba(68,68,68,.2)_50%,transparent_75%,transparent_100%)] bg-[length:250%_250%,100%_100%] animate-[shine_3s_infinite] pointer-events-none"></div>
      <div class="relative z-10 space-y-6">
        <h3 class="text-2xl md:text-3xl font-black leading-tight">로그인하고 나만의<br>맞춤 상품을 추천받으세요</h3>
        <p class="text-slate-400 font-medium">내 자산 상황에 딱 맞는 최고의 금리 상품을 AI가 찾아드립니다.</p>
        <button @click="$router.push('/login')" class="mt-4 px-10 py-4 bg-white text-slate-900 hover:bg-slate-100 rounded-full font-black text-lg transition-all hover:shadow-xl hover:shadow-white/10 transform hover:-translate-y-1">
          지금 시작하기
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
@keyframes shine {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>