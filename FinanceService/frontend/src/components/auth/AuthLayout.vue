<template>
  <div class="min-h-[calc(100vh-80px)] bg-slate-50 flex items-center justify-center p-6">
    <div class="w-full max-w-[440px]">
      <div class="text-center mb-10">
        <router-link to="/" class="inline-flex items-center gap-2 mb-4 group">
          <span class="text-3xl group-hover:scale-110 transition-transform">🐜</span>
          <span class="text-2xl font-black text-slate-800 tracking-tighter">Smart <span class="text-primary">Ants</span></span>
        </router-link>
        <h2 class="text-xl font-bold text-slate-500"><slot name="title"></slot></h2>
      </div>
      
      <div class="bg-white p-10 rounded-[2.5rem] shadow-xl shadow-slate-200/60 border border-slate-100">
        <slot name="form"></slot>
      </div>
    </div>
  </div>
</template>