<script setup>
import { ref } from 'vue'
const props = defineProps({ initialData: Object })
const emit = defineEmits(['submit'])

const form = ref({ ...props.initialData })

const onSubmit = () => emit('submit', form.value)
</script>

<template>
  <form @submit.prevent="onSubmit" class="space-y-6">
    <div class="space-y-2">
      <label class="text-xs font-black text-slate-400 ml-1">닉네임</label>
      <input v-model="form.nickname" type="text" class="input input-bordered w-full rounded-2xl bg-slate-50 border-slate-200 focus:border-primary font-bold" />
    </div>
    <div class="space-y-2">
      <label class="text-xs font-black text-slate-400 ml-1">연봉 (원)</label>
      <input v-model="form.salary" type="number" class="input input-bordered w-full rounded-2xl bg-slate-50 border-slate-200 focus:border-primary font-bold" />
    </div>
    <div class="space-y-2">
      <label class="text-xs font-black text-slate-400 ml-1 block text-center">투자 성향 ({{ form.risk_appetite }}단계)</label>
      <input v-model="form.risk_appetite" type="range" min="1" max="5" class="range range-primary range-sm" step="1" />
    </div>
    <button type="submit" class="btn btn-primary w-full h-14 rounded-2xl text-lg font-black shadow-lg shadow-primary/30 mt-4">
      정보 수정 완료
    </button>
  </form>
</template>