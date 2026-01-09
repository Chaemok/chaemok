<script setup>
import { useFinanceStore } from '@/stores/finance'

const props = defineProps({
  type: String, // '예금' 또는 '적금'
  products: {
      type: Array,
      default: () => []
  } 
})

const store = useFinanceStore()

// 🐜 가입 취소 핸들러
const handleCancel = async (item) => {
    const productName = item.product?.fin_prdt_nm || '상품'
    
    // 🔍 디버깅용 로그 추가: item.id가 실제로 존재하는 값인지 확인
    console.log('해지 요청 아이템:', item)
    console.log('전송되는 ID:', item.id)

    if (!confirm(`정말 [${productName}] 가입을 해지하시겠습니까?`)) return

    try {
        if (props.type === '예금') {
            // item.id가 아니라 item.option_id 혹은 다른 필드여야 할 수도 있습니다.
            await store.toggleDepositJoin(item.id) 
        } else {
            await store.toggleSavingJoin(item.id)
        }
        alert('해지가 완료되었습니다.')
    } catch (err) {
        // ... 생략
    }
}
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center gap-2 mb-4">
      <span class="text-2xl">{{ type === '예금' ? '💰' : '🐖' }}</span>
      <h3 class="text-lg font-black text-slate-800">가입한 {{ type }}</h3>
    </div>

    <div v-if="products.length > 0" class="grid gap-4 md:grid-cols-2">
      <div 
        v-for="item in products" 
        :key="item.id" 
        class="group relative bg-white border border-slate-100 rounded-2xl p-6 hover:shadow-lg hover:border-blue-100 transition-all duration-300"
      >
        <div class="flex justify-between items-start mb-4">
          <div class="space-y-1">
            <span class="text-xs font-bold text-slate-400 bg-slate-50 px-2 py-1 rounded mb-1 inline-block">
              {{ item.product?.kor_co_nm || '금융사' }}
            </span>
            <h4 class="font-black text-slate-900 text-lg group-hover:text-blue-600 transition-colors line-clamp-1">
              {{ item.product?.fin_prdt_nm || '상품명 없음' }}
            </h4>
            
            <div class="flex items-center gap-2 mt-2">
              <span class="px-2 py-0.5 rounded-md text-xs font-bold border"
                    :class="type === '예금' ? 'bg-blue-50 text-blue-600 border-blue-100' : 'bg-purple-50 text-purple-600 border-purple-100'">
                {{ item.save_trm }}개월
              </span>
            </div>
          </div>
          
          <div class="text-center bg-slate-50 rounded-xl p-3 min-w-[70px]">
            <p class="text-[10px] text-slate-400 font-bold uppercase">최고</p>
            <p class="text-lg font-black"
               :class="type === '예금' ? 'text-blue-600' : 'text-purple-600'">
               {{ item.intr_rate2 }}%
            </p>
          </div>
        </div>

        <div class="flex justify-between items-end pt-2 border-t border-slate-50 mt-2">
             <span class="text-xs font-bold text-slate-400">기본 연 {{ item.intr_rate }}%</span>
             
             <button 
                @click.stop="handleCancel(item)"
                class="px-3 py-1.5 rounded-lg bg-slate-100 text-slate-500 text-xs font-bold hover:bg-rose-100 hover:text-rose-600 transition-colors z-10"
             >
                해지하기
             </button>
        </div>

      </div>
    </div>

    <div v-else class="py-12 text-center bg-slate-50 rounded-3xl border border-dashed border-slate-200">
      <p class="text-slate-400 font-bold text-sm">가입한 {{ type }} 상품이 없습니다.</p>
    </div>
  </div>
</template>