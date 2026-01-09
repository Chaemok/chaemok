<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  initialData: Object
})
const emit = defineEmits(['submit'])

// 초기값 설정 (부모로부터 받은 initialData가 있으면 그걸 쓰고, 없으면 기본값)
const form = ref({
  nickname: '',
  money: 0,
  salary: 0,
  birth_date: '',
  risk_appetite: 3, // 기본값 3 (위험중립형)
  job: 'etc',
})

// initialData가 로드되면 form에 채워넣기
watch(() => props.initialData, (newData) => {
  if (newData) {
    form.value = {
      ...form.value, // 기본값 유지하면서
      ...newData,    // 받아온 값 덮어쓰기
      // birth_date나 null 값 처리
      birth_date: newData.birth_date || '',
      money: newData.money || 0,
      salary: newData.salary || 0,
    }
  }
}, { immediate: true })

const onSubmit = () => {
  // 숫자형 데이터 변환 안전장치
  const payload = {
    ...form.value,
    money: Number(form.value.money),
    salary: Number(form.value.salary),
    risk_appetite: Number(form.value.risk_appetite)
  }
  emit('submit', payload)
}
</script>

<template>
  <form @submit.prevent="onSubmit" class="space-y-8 animate-in slide-in-from-bottom-2 duration-500">
    
    <div class="space-y-2">
      <label class="text-xs font-black text-slate-400 ml-1 uppercase tracking-widest">닉네임</label>
      <input v-model="form.nickname" type="text" placeholder="닉네임을 입력하세요"
             class="w-full h-14 px-5 rounded-2xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-blue-500 font-bold outline-none transition-all" />
    </div>

    <div class="grid grid-cols-2 gap-4">
      <div class="space-y-2">
        <label class="text-xs font-black text-slate-400 ml-1 uppercase tracking-widest">운용 자산 (원)</label>
        <input v-model.number="form.money" type="number" placeholder="0"
               class="w-full h-14 px-5 rounded-2xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-blue-500 font-bold outline-none transition-all" />
      </div>

      <div class="space-y-2">
        <label class="text-xs font-black text-slate-400 ml-1 uppercase tracking-widest">연봉 (원)</label>
        <input v-model.number="form.salary" type="number" placeholder="0"
               class="w-full h-14 px-5 rounded-2xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-blue-500 font-bold outline-none transition-all" />
      </div>
    </div>

    <div class="space-y-2">
      <label class="text-xs font-black text-slate-400 ml-1 uppercase tracking-widest">생년월일</label>
      <input v-model="form.birth_date" type="date"
             class="w-full h-14 px-5 rounded-2xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-blue-500 font-bold text-slate-600 outline-none transition-all" />
    </div>
    
    <div class="space-y-2">
        <label class="text-xs font-black text-slate-400 ml-1 uppercase tracking-widest">직업</label>
        <select v-model="form.job" class="w-full h-14 px-5 rounded-2xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-blue-500 font-bold text-slate-600 outline-none appearance-none cursor-pointer">
            <option value="student">학생</option>
            <option value="employee">직장인</option>
            <option value="civil_servant">공무원</option>
            <option value="professional">전문직</option>
            <option value="freelancer">프리랜서</option>
            <option value="business">사업자</option>
            <option value="housewife">주부</option>
            <option value="unemployed">무직</option>
            <option value="etc">기타</option>
        </select>
    </div>

    <div class="space-y-4 pt-4 bg-slate-50 p-6 rounded-3xl border border-slate-100">
      <div class="flex justify-between items-end px-1">
        <label class="text-xs font-black text-slate-400 uppercase tracking-widest">투자 성향</label>
        <span class="text-sm font-black text-blue-600 bg-white border border-blue-100 px-3 py-1 rounded-full shadow-sm">
          {{ form.risk_appetite }}단계 : 
          <span v-if="form.risk_appetite == 1">안정형 🐢</span>
          <span v-else-if="form.risk_appetite == 2">안정추구형 🐇</span>
          <span v-else-if="form.risk_appetite == 3">위험중립형 🦊</span>
          <span v-else-if="form.risk_appetite == 4">적극투자형 🐯</span>
          <span v-else>공격투자형 🦅</span>
        </span>
      </div>
      <input v-model.number="form.risk_appetite" type="range" min="1" max="5" step="1" 
             class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600" />
      <div class="flex justify-between text-[10px] text-slate-400 font-bold px-1">
        <span>안정형</span>
        <span>공격형</span>
      </div>
    </div>

    <div class="pt-4">
      <button type="submit" class="w-full h-14 rounded-2xl bg-slate-900 text-white font-bold text-lg hover:bg-blue-600 shadow-xl shadow-slate-200 transition-all active:scale-[0.98]">
        변경사항 저장하기
      </button>
    </div>
  </form>
</template>