<template>
  <div class="fixed inset-0 z-[9999] flex items-center justify-center bg-white font-pretendard">
    <div class="text-center relative z-10">
      
      <div class="flex flex-col items-center justify-center gap-6 mb-10">
        <div class="w-24 h-24 bg-slate-900 rounded-[2rem] flex items-center justify-center shadow-2xl shadow-blue-500/30 animate-bounce-custom">
          <span class="text-6xl">🐜</span>
        </div>
        
        <div class="space-y-2">
          <h1 class="text-5xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600 animate-fade-up">
            Smart Ants
          </h1>
          <p class="text-sm font-bold text-slate-400 tracking-[0.3em] uppercase animate-fade-up delay-100">
            Financial Intelligence
          </p>
        </div>
      </div>

      <div class="w-[180px] h-1.5 bg-slate-100 rounded-full overflow-hidden mx-auto relative">
        <div class="loading-bar"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 로딩바 애니메이션 + 투톤 그라데이션 */
.loading-bar {
  /* Tailwind 클래스를 직접 적용하거나 @apply 사용 (환경에 따라 선택) */
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: linear-gradient(to right, #2563eb, #4f46e5, #7c3aed); /* Blue-600 -> Violet-600 */
  border-radius: 9999px;
  transform-origin: left;
  animation: load-progress 1.5s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

@keyframes bounce-custom {
  0% { transform: scale(0); opacity: 0; }
  50% { transform: scale(1.1); opacity: 1; }
  70% { transform: scale(0.95); }
  100% { transform: scale(1); }
}

@keyframes fade-up {
  0% { transform: translateY(20px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}

@keyframes load-progress {
  0% { transform: scaleX(0); }
  50% { transform: scaleX(0.7); }
  100% { transform: scaleX(1); }
}

.delay-100 { animation-delay: 0.1s; }
</style>