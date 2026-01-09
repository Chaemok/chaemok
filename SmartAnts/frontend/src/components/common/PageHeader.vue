<script setup>
defineProps({
  title: String,
  subtitle: String,
  bgClass: { // 배경색이나 그라데이션 커스텀용
    type: String,
    default: 'bg-slate-900'
  }
})
</script>

<template>
  <div :class="['relative w-full h-[200px] md:h-[250px] flex items-center justify-center text-center px-6 overflow-hidden mb-12', bgClass]">
    
    <div class="absolute inset-0 opacity-20 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]"></div>
    <div class="absolute inset-0 bg-gradient-to-t from-slate-950/50 to-transparent"></div>

    <div class="relative z-10 text-white space-y-4 max-w-2xl animate-fade-in-up">
      <h1 class="text-3xl md:text-4xl font-black tracking-tight">{{ title }}</h1>
      <p class="text-slate-300 font-medium md:text-lg">{{ subtitle }}</p>
    </div>
  </div>
</template>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
}
</style>