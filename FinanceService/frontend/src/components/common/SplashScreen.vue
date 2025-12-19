<template>
  <div class="splash-container">
    <div class="logo-wrapper">
      <h1 class="logo-text">Smart Ants</h1>
      <div class="loading-bar"></div>
    </div>
  </div>
</template>

<style scoped>
.splash-container {
  @apply fixed inset-0 z-[9999] flex items-center justify-center bg-white;
}
.logo-text {
  @apply text-5xl font-black italic tracking-tighter text-emerald-500;
  animation: logo-pop 1s ease-out forwards;
}
.loading-bar {
  @apply mt-4 h-1 w-0 bg-emerald-500 rounded-full;
  animation: load 1.5s ease-in-out forwards;
}

@keyframes logo-pop {
  0% { transform: scale(0.5); opacity: 0; filter: blur(10px); }
  100% { transform: scale(1); opacity: 1; filter: blur(0); }
}
@keyframes load {
  0% { width: 0%; }
  100% { width: 100%; }
}
</style>