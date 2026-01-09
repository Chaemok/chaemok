<script setup>
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  product: { type: Object, required: true },
  isOpen: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'join'])
const authStore = useAuthStore()

const handleJoin = (optionPk) => {
  if (!authStore.isLoggedIn) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }
  if (confirm('이 상품에 가입하시겠습니까?')) {
    emit('join', optionPk)
  }
}
</script>

<template>
  <dialog :open="isOpen" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box max-w-2xl bg-white rounded-[2.5rem] p-0 overflow-hidden shadow-2xl">
      <div class="bg-slate-50 p-8 border-b border-slate-100 relative">
        <button @click="$emit('close')" class="btn btn-sm btn-circle btn-ghost absolute right-4 top-4 text-slate-400">✕</button>
        <div class="flex items-center gap-5 mb-4">
          <div class="w-16 h-16 bg-white rounded-2xl shadow-sm border border-slate-100 flex items-center justify-center text-3xl">🏛️</div>
          <div>
            <p class="text-sm font-bold text-primary mb-1">{{ product.kor_co_nm }}</p>
            <h3 class="text-2xl font-black text-slate-800 tracking-tight">{{ product.fin_prdt_nm }}</h3>
          </div>
        </div>
        <div class="flex gap-2">
          <span class="badge badge-ghost border-slate-200 text-slate-500 font-medium py-3 px-4">{{ product.join_member }}</span>
          <span class="badge badge-primary badge-outline font-medium py-3 px-4">D-Day 특판</span>
        </div>
      </div>

      <div class="p-8 space-y-8">
        <div class="space-y-3">
          <h4 class="flex items-center gap-2 font-bold text-slate-800">
            <span class="w-1 h-4 bg-primary rounded-full"></span> 상품 특징
          </h4>
          <p class="text-sm text-slate-500 leading-relaxed pl-3 italic">{{ product.etc_note }}</p>
        </div>

        <div class="space-y-4">
          <h4 class="flex items-center gap-2 font-bold text-slate-800">
            <span class="w-1 h-4 bg-primary rounded-full"></span> 기간별 금리 (세전)
          </h4>
          <div class="overflow-x-auto border border-slate-100 rounded-3xl bg-white">
            <table class="table w-full">
              <thead>
                <tr class="bg-slate-50 text-slate-400 border-b border-slate-100">
                  <th class="py-4 pl-6">저축 기간</th>
                  <th>기본 금리</th>
                  <th>최고 우대금리</th>
                  <th class="pr-6 text-center">신청</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="opt in product.options" :key="opt.id" class="border-b border-slate-50 last:border-none hover:bg-slate-50/50 transition-colors">
                  <td class="py-4 pl-6 font-bold text-slate-700">{{ opt.save_trm }}개월</td>
                  <td class="text-slate-500 font-medium">{{ opt.intr_rate }}%</td>
                  <td class="text-primary font-black text-lg">{{ opt.intr_rate2 }}%</td>
                  <td class="pr-6 text-center">
                    <button @click="handleJoin(opt.id)" class="btn btn-primary btn-sm rounded-xl px-5 shadow-sm shadow-primary/20">가입</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="bg-slate-50 p-5 rounded-3xl flex items-start gap-3 border border-slate-100">
          <span class="text-xl">📢</span>
          <div class="space-y-1">
            <p class="text-xs font-bold text-slate-700">우대 조건 및 유의사항</p>
            <p class="text-[11px] text-slate-400 leading-relaxed">{{ product.spcl_cnd }}</p>
          </div>
        </div>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button @click="$emit('close')">close</button>
    </form>
  </dialog>
</template>