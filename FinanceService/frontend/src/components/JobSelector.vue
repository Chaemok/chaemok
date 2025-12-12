<script setup>
// 부모로부터 선택된 값(modelValue)을 받습니다 (v-model 원리)
defineProps(['modelValue'])
defineEmits(['update:modelValue'])

// 옵션 리스트를 여기서만 관리합니다. (나중에 수정할 때 여기만 고치면 됨!)
const jobOptions = [
  { value: 'student', label: '학생' },
  { value: 'employee', label: '직장인' },
  { value: 'civil_servant', label: '공무원' },
  { value: 'professional', label: '전문직' },
  { value: 'freelancer', label: '프리랜서' },
  { value: 'business', label: '사업자' },
  { value: 'housewife', label: '주부' },
  { value: 'unemployed', label: '무직' },
  { value: 'etc', label: '기타' },
]
</script>

<template>
  <div class="form-control w-full">
    <label class="label font-bold text-sm">직업</label>
    <select 
      :value="modelValue" 
      @change="$emit('update:modelValue', $event.target.value)"
      class="select select-bordered w-full"
    >
      <option disabled value="">직업을 선택해주세요</option>
      <option v-for="opt in jobOptions" :key="opt.value" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>
  </div>
</template>