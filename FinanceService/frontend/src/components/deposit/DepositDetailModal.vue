<script setup>
// 부모로부터 상태와 데이터를 받음
const props = defineProps({
  isOpen: Boolean,
  product: Object
})
const emit = defineEmits(['close'])
</script>

<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="emit('close')">
      <div class="bg-white w-full max-w-2xl rounded-[3rem] overflow-hidden shadow-2xl animate-modal-up">
        
        <div class="p-8 bg-indigo-600 text-white relative">
          <button @click="emit('close')" class="absolute top-6 right-6 text-white/50 hover:text-white transition-colors">✕</button>
          <p class="text-xs font-bold opacity-80 mb-2 tracking-widest uppercase">{{ product?.kor_co_nm }}</p>
          <h2 class="text-3xl font-black leading-tight">{{ product?.fin_prdt_nm }}</h2>
        </div>

        <div class="p-10 space-y-8 max-h-[60vh] overflow-y-auto custom-scrollbar">
          <div class="grid grid-cols-2 gap-8">
            <div class="space-y-2">
              <h4 class="text-[10px] font-black text-slate-400 uppercase tracking-widest">가입 대상</h4>
              <p class="font-bold text-slate-700 leading-snug">{{ product?.join_member || '제한 없음' }}</p>
            </div>
            <div class="space-y-2">
              <h4 class="text-[10px] font-black text-slate-400 uppercase tracking-widest">가입 방법</h4>
              <p class="font-bold text-slate-700 leading-snug">{{ product?.join_way }}</p>
            </div>
          </div>

          <div v-if="product?.options?.length">
            <h4 class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-4">저축 기간별 금리 상세</h4>
            <div class="border border-slate-100 rounded-2xl overflow-hidden shadow-sm">
              <table class="w-full text-sm">
                <thead class="bg-slate-50 border-b border-slate-100">
                  <tr class="text-slate-400 font-black text-[10px] uppercase">
                    <th class="py-4 px-6 text-left">기간</th>
                    <th class="py-4 px-6 text-center">기본 금리</th>
                    <th class="py-4 px-6 text-right">최고 우대금리</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                  <tr v-for="opt in product?.options" :key="opt.id" class="hover:bg-slate-50/50 transition-colors">
                    <td class="py-4 px-6 font-bold text-slate-600">{{ opt.save_trm }}개월</td>
                    <td class="py-4 px-6 text-center font-black text-slate-800">{{ opt.intr_rate }}%</td>
                    <td class="py-4 px-6 text-right font-black text-indigo-600">{{ opt.intr_rate2 }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="product?.etc_note" class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
            <h4 class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-3">상품 유의사항</h4>
            <p class="text-xs text-slate-500 leading-relaxed">{{ product.etc_note }}</p>
          </div>
        </div>

        <div class="p-8 border-t border-slate-50 flex gap-4 bg-white">
          <button @click="emit('close')" class="flex-1 py-4 text-slate-400 font-black hover:bg-slate-50 rounded-2xl transition-all">닫기</button>
          <button class="flex-[2] py-4 bg-indigo-600 text-white font-black rounded-2xl shadow-lg shadow-indigo-100 hover:bg-indigo-700 transition-all hover:-translate-y-1">
            이 상품 가입하기 🐜
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }
.animate-modal-up { animation: modalUp 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
@keyframes modalUp {
  from { opacity: 0; transform: translateY(40px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>