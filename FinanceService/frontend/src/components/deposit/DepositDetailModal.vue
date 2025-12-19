<script setup>
import BaseModal from '@/components/common/BaseModal.vue'

defineProps({
  product: Object,
  isOpen: Boolean
})
defineEmits(['close'])
</script>

<template>
  <BaseModal :is-open="isOpen" @close="$emit('close')">
    <template #header>
      <p class="text-sm font-black text-primary mb-1">{{ product.kor_co_nm }}</p>
      <h2 class="text-3xl font-black text-slate-800">{{ product.fin_prdt_nm }}</h2>
    </template>

    <template #body>
      <div class="grid grid-cols-2 gap-6 mb-8">
        <div class="bg-slate-50 p-6 rounded-[2rem] text-center">
          <p class="text-xs text-slate-400 font-bold mb-1 uppercase">기본 금리</p>
          <p class="text-3xl font-black text-slate-700">{{ product.intr_rate }}%</p>
        </div>
        <div class="bg-indigo-50 p-6 rounded-[2rem] text-center">
          <p class="text-xs text-primary font-bold mb-1 uppercase">우대 금리</p>
          <p class="text-3xl font-black text-primary">{{ product.max_intr_rate }}%</p>
        </div>
      </div>
      <p class="bg-slate-50 p-8 rounded-[2rem] text-sm leading-relaxed whitespace-pre-wrap">
        {{ product.etc_note }}
      </p>
    </template>

    <template #footer>
      <button @click="$emit('close')" class="btn btn-ghost flex-1 rounded-2xl font-bold">닫기</button>
      <button class="btn btn-primary flex-[2] rounded-2xl font-black text-lg shadow-lg shadow-primary/20">
        상품 가입하기 🐜
      </button>
    </template>
  </BaseModal>
</template>