<template>
  <div class="join w-full justify-end">
    <input 
      v-model="keyword"
      class="input input-bordered join-item w-full max-w-xs focus:outline-none focus:border-primary" 
      :placeholder="placeholder"
      @keyup.enter="triggerSearch"
    />
    
    <button 
      class="btn btn-primary join-item text-white"
      @click="triggerSearch"
    >
      검색 🔍
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  placeholder: {
    type: String,
    default: '검색어를 입력하세요'
  }
})

const emit = defineEmits(['search'])
const keyword = ref('')

const triggerSearch = () => {
  // 부모에게 검색어 전달
  emit('search', keyword.value)
}
</script>