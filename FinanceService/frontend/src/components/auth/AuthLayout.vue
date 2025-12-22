<template>
  <div class="min-h-[calc(100vh-80px)] bg-background flex items-center justify-center p-6 antialiased">
    <div class="w-full max-w-[400px] animate-layout-entry">
      
      <div class="text-center mb-10">
        <router-link to="/" class="inline-flex items-center gap-3 mb-6 group">
          <div class="w-10 h-10 bg-slate-900 rounded-xl flex items-center justify-center group-hover:bg-blue-600 transition-colors duration-500 shadow-lg shadow-slate-200">
            <span class="text-xl group-hover:scale-110 transition-transform">🐜</span>
          </div>
          <span class="text-xl font-black text-slate-900 tracking-tighter">
            Smart <span class="text-primary">Ants</span>
          </span>
        </router-link>
        
        <h1 class="text-2xl font-semibold tracking-tight text-slate-900 mb-2">
          <slot name="title"></slot>
        </h1>
        <p class="text-sm text-slate-400 font-medium">
          스마트한 개미들의 금융 커뮤니티
        </p>
      </div>
      
      <div class="bg-card p-8 md:p-10 rounded-[24px] border border-slate-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] relative overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-blue-500/20 to-transparent"></div>
        <slot name="form"></slot>
      </div>

      <div class="mt-8 text-center">
        <p class="text-[10px] text-slate-300 font-bold uppercase tracking-[0.2em]">
          &copy; 2025 Smart Ants
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 🐜 밋밋함을 깨는 고급스러운 가속도 곡선 */
.animate-layout-entry {
  animation: slideUpExpo 1.2s cubic-bezier(0.19, 1, 0.22, 1) forwards;
}

@keyframes slideUpExpo {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>