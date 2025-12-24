<script setup>
defineProps({
  isOpen: Boolean,
  videoId: String
})
defineEmits(['close'])
</script>

<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/90 p-4 backdrop-blur-sm" @click.self="$emit('close')">
      <div class="w-full max-w-4xl aspect-video bg-black rounded-2xl overflow-hidden shadow-2xl relative animate-up">
        <iframe 
          class="w-full h-full"
          :src="`https://www.youtube.com/embed/${videoId}?autoplay=1`" 
          title="YouTube video player" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
          allowfullscreen
        ></iframe>
        <button @click="$emit('close')" class="absolute -top-12 right-0 text-white/70 hover:text-white text-lg font-bold flex items-center gap-2 transition-colors">
          닫기 ✕
        </button>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
@keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; }}
.animate-up { animation: slideUp 0.4s ease-out; }
</style>