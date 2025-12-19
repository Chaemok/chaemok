<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import api from '@/api'; // 기존에 설정한 axios 인스턴스 사용
import { useFinanceStore } from '@/stores/finance';

const financeStore = useFinanceStore();

// ==========================================
// 🚨 [필수 설정] 카카오 앱 키 (하드코딩)
// ==========================================
const KAKAO_MAP_JS_KEY = '23fbca3b74e77ccdfc30b0024a5256cf';

// ==========================================
// 정적 데이터 (지역 및 금융기관)
// ==========================================
const staticData = {
  "koreaAreas": {
    "서울": ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"],
    "경기": ["수원시 장안구", "수원시 권선구", "수원시 팔달구", "수원시 영통구", "성남시 수정구", "성남시 중원구", "성남시 분당구", "의정부시", "안양시 만안구", "안양시 동안구", "부천시", "광명시", "평택시", "동두천시", "안산시 상록구", "안산시 단원구", "고양시 덕양구", "고양시 일산동구", "고양시 일산서구", "과천시", "구리시", "남양주시", "오산시", "시흥시", "군포시", "의왕시", "하남시", "용인시 처인구", "용인시 기흥구", "용인시 수지구", "파주시", "이천시", "안성시", "김포시", "화성시", "광주시", "양주시", "포천시", "여주시", "연천군", "가평군", "양평군"],
    "부산": ["강서구", "금정구", "기장군", "남구", "동구", "동래구", "부산진구", "북구", "사상구", "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구"],
    "인천": ["계양구", "남동구", "동구", "미추홀구", "부평구", "서구", "연수구", "중구", "강화군", "옹진군"],
    "대구": ["남구", "달서구", "달성군", "동구", "북구", "서구", "수성구", "중구", "군위군"],
    "대전": ["대덕구", "동구", "서구", "유성구", "중구"],
    "광주": ["광산구", "남구", "동구", "북구", "서구"],
    "울산": ["남구", "동구", "북구", "울주군", "중구"],
    "세종": ["세종특별자치시"],
    "강원": ["강릉시", "동해시", "삼척시", "속초시", "원주시", "춘천시", "태백시", "고성군", "양구군", "양양군", "영월군", "인제군", "정선군", "철원군", "평창군", "홍천군", "화천군", "횡성군"],
    "충북": ["청주시 상당구", "청주시 서원구", "청주시 흥덕구", "청주시 청원구", "충주시", "제천시", "보은군", "옥천군", "영동군", "증평군", "진천군", "괴산군", "음성군", "단양군"],
    "충남": ["천안시 동남구", "천안시 서북구", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시", "금산군", "부여군", "서천군", "청양군", "홍성군", "예산군", "태안군"],
    "경북": ["포항시 남구", "포항시 북구", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시", "상주시", "문경시", "경산시", "의성군", "청송군", "영양군", "영덕군", "청도군", "고령군", "성주군", "칠곡군", "예천군", "봉화군", "울진군", "울릉군"],
    "경남": ["창원시 의창구", "창원시 성산구", "창원시 마산합포구", "창원시 마산회원구", "창원시 진해구", "진주시", "통영시", "사천시", "김해시", "밀양시", "거제시", "양산시", "의령군", "함안군", "창녕군", "고성군", "남해군", "하동군", "산청군", "함양군", "거창군", "합천군"],
    "전북": ["전주시 완산구", "전주시 덕진구", "군산시", "익산시", "정읍시", "남원시", "김제시", "완주군", "진안군", "무주군", "장수군", "임실군", "순창군", "고창군", "부안군"],
    "전남": ["목포시", "여수시", "순천시", "나주시", "광양시", "담양군", "곡성군", "구례군", "고흥군", "보성군", "화순군", "장흥군", "강진군", "해남군", "영암군", "무안군", "함평군", "영광군", "장성군", "완도군", "진도군", "신안군"],
    "제주": ["제주시", "서귀포시"]
  },
  "financialInstitutions": [
    { "name": "KB국민은행", "type": "BANK" }, { "name": "신한은행", "type": "BANK" }, { "name": "우리은행", "type": "BANK" },
    { "name": "하나은행", "type": "BANK" }, { "name": "NH농협은행", "type": "BANK" }, { "name": "IBK기업은행", "type": "BANK" },
    { "name": "우체국", "type": "BANK" }, { "name": "새마을금고", "type": "BANK" }, { "name": "신협", "type": "BANK" },
    { "name": "키움증권", "type": "SEC" }, { "name": "미래에셋증권", "type": "SEC" }, { "name": "삼성증권", "type": "SEC" }
  ]
};

// ==========================================
// 지도 및 검색 상태
// ==========================================
const mapContainer = ref(null); 
const map = ref(null);
const geocoder = ref(null);
const infowindow = ref(null);
const markers = ref([]);
const loading = ref(false);
const placesData = ref([]);

// 필터 상태
const selectedSido = ref('');
const selectedGugun = ref('');
const selectedType = ref('BANK'); 
const selectedBank = ref('ALL_BANK'); 
const locationBias = ref('MY_LOCATION'); 

// ==========================================
// Computed (필터 로직)
// ==========================================
const gugunOptions = computed(() => selectedSido.value ? staticData.koreaAreas[selectedSido.value] : []);

const bankOptions = computed(() => {
  let options = [];
  if (selectedType.value === 'BANK') {
    options.push({ value: 'ALL_BANK', text: '전체 은행' });
    options.push(...staticData.financialInstitutions.filter(i => i.type === 'BANK').map(i => ({ value: i.name, text: i.name })));
  } else if (selectedType.value === 'SEC') {
    options.push({ value: 'ALL_SEC', text: '전체 증권사' });
    options.push(...staticData.financialInstitutions.filter(i => i.type === 'SEC').map(i => ({ value: i.name, text: i.name })));
  } else if (selectedType.value === 'ATM') {
    options.push({ value: 'ALL_ATM', text: '전체 ATM' });
  }
  return options;
});

watch(selectedSido, () => selectedGugun.value = '');
watch(selectedType, () => selectedBank.value = bankOptions.value[0]?.value || '');

// ==========================================
// 지도 기능 함수
// ==========================================
const clearMarkers = () => {
  markers.value.forEach(m => m.setMap(null));
  markers.value = [];
};

const displayPlaces = (places) => {
  clearMarkers();
  if (!map.value || places.length === 0) return;
  const bounds = new window.kakao.maps.LatLngBounds();

  places.forEach((place) => {
    const pos = new window.kakao.maps.LatLng(place.y, place.x); 
    const marker = new window.kakao.maps.Marker({
      map: map.value,
      position: pos
    });
    markers.value.push(marker);
    bounds.extend(pos);

    window.kakao.maps.event.addListener(marker, 'click', () => {
      map.value.panTo(pos);
      const content = `<div class="p-2 text-xs font-bold text-slate-800">${place.name}</div>`;
      infowindow.value.setContent(content);
      infowindow.value.open(map.value, marker);
    });
  });
  map.value.setBounds(bounds);
};

const initMap = () => {
  if (!window.kakao || !mapContainer.value) return;
  window.kakao.maps.load(() => {
    const options = { center: new window.kakao.maps.LatLng(37.5665, 126.9780), level: 4 };
    map.value = new window.kakao.maps.Map(mapContainer.value, options);
    geocoder.value = new window.kakao.maps.services.Geocoder();
    infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 1 });
    moveToMyLocation();
  });
};

const moveToMyLocation = () => {
  if (navigator.geolocation && map.value) {
    navigator.geolocation.getCurrentPosition((pos) => {
      const loc = new window.kakao.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
      map.value.setCenter(loc);
      locationBias.value = `${pos.coords.latitude},${pos.coords.longitude}`;
    });
  }
};

const executeSearch = () => {
  loading.value = true;
  let finalQuery = selectedBank.value.startsWith('ALL') 
                   ? (selectedType.value === 'BANK' ? '은행' : selectedType.value === 'SEC' ? '증권사' : 'ATM') 
                   : selectedBank.value;
  
  if (selectedSido.value) {
    const address = selectedSido.value + (selectedGugun.value ? ' ' + selectedGugun.value : '');
    geocoder.value.addressSearch(address, (result, status) => {
      if (status === window.kakao.maps.services.Status.OK) {
        locationBias.value = `${result[0].y},${result[0].x}`;
        searchPlacesApi(finalQuery);
      }
    });
  } else {
    searchPlacesApi(finalQuery);
  }
};

const searchPlacesApi = async (query) => {
  loading.value = true;
  
  // locationBias는 "lat,lng" 형태이므로 분리해서 백엔드 규격에 맞게 전달
  const [lat, lng] = locationBias.value.split(',');

  try {
    const response = await api.get('finlife/map-search/', {
      params: {
        query: query,
        lat: lat,
        lng: lng,
        type: selectedType.value.toLowerCase() // 'bank', 'atm', 'sec'
      }
    });

    // 백엔드 응답(response.data)에 'documents'가 포함되어 있는지 확인
    if (response.data && response.data.documents) {
      placesData.value = response.data.documents.map(p => ({
        id: p.id,
        name: p.place_name,
        address: p.address_name,
        x: p.x, // 경도
        y: p.y, // 위도
        category_name: p.category_name,
        distance: p.distance
      }));
      displayPlaces(placesData.value);
    }
  } catch (error) {
    console.error('API 호출 중 오류 발생:', error);
    // image_4a61a4.png의 Connection Refused 에러 대응
    if (error.code === 'ERR_NETWORK') {
      alert("백엔드 서버(Django)가 실행 중인지 확인해 주세요!");
    }
  } finally {
    loading.value = false;
  }
};



onMounted(() => initMap());
</script>

<template>
  <div class="flex h-[calc(100vh-80px)] w-full overflow-hidden bg-slate-50">
    <aside class="w-[400px] bg-white border-r border-slate-100 flex flex-col shadow-xl z-10">
      <div class="p-6 space-y-6 border-b border-slate-50">
        <h2 class="text-2xl font-black text-slate-800 tracking-tight">주변 은행 찾기 📍</h2>
        
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-2">
            <select v-model="selectedSido" class="select select-bordered rounded-xl select-sm focus:border-primary">
              <option value="">시/도 선택</option>
              <option v-for="(_, sido) in staticData.koreaAreas" :key="sido" :value="sido">{{ sido }}</option>
            </select>
            <select v-model="selectedGugun" class="select select-bordered rounded-xl select-sm focus:border-primary">
              <option value="">구/군 선택</option>
              <option v-for="gugun in gugunOptions" :key="gugun" :value="gugun">{{ gugun }}</option>
            </select>
          </div>

          <div class="flex bg-slate-100 p-1 rounded-xl">
            <button v-for="t in ['BANK', 'SEC', 'ATM']" :key="t" 
                    @click="selectedType = t"
                    :class="selectedType === t ? 'bg-white text-primary shadow-sm' : 'text-slate-400'"
                    class="flex-1 py-1.5 text-xs font-bold rounded-lg transition-all">
              {{ t === 'BANK' ? '은행' : t === 'SEC' ? '증권' : 'ATM' }}
            </button>
          </div>

          <div class="flex gap-2">
            <select v-model="selectedBank" class="select select-bordered rounded-xl select-sm flex-1 focus:border-primary">
              <option v-for="opt in bankOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
            </select>
            <button @click="executeSearch" class="btn btn-primary btn-sm rounded-xl px-6" :disabled="loading">
              <span v-if="loading" class="loading loading-spinner loading-xs"></span>
              <span v-else>검색</span>
            </button>
          </div>
        </div>
      </div>

      <div class="flex-1 overflow-y-auto p-6 space-y-4">
        <div v-if="placesData.length === 0 && !loading" class="text-center py-20 text-slate-400 space-y-2">
          <p class="text-4xl">🐜</p>
          <p class="text-sm font-medium">검색 결과가 없습니다.</p>
        </div>

        <div v-for="place in placesData" :key="place.id" 
             @click="map.panTo(new window.kakao.maps.LatLng(place.y, place.x))"
             class="card border border-slate-100 p-5 rounded-[1.5rem] hover:border-primary hover:shadow-md transition-all cursor-pointer group">
          <p class="text-[10px] font-bold text-primary mb-1">{{ place.category_name?.split(' > ').pop() }}</p>
          <h4 class="font-bold text-slate-700 group-hover:text-primary transition-colors">{{ place.name }}</h4>
          <p class="text-xs text-slate-400 mt-2">{{ place.address }}</p>
          <div class="flex justify-between items-center mt-4">
            <span class="text-[10px] text-slate-300">{{ place.distance ? place.distance + 'm' : '' }}</span>
            <button class="btn btn-xs btn-ghost text-primary">지도보기</button>
          </div>
        </div>
      </div>
    </aside>

    <main class="flex-1 relative">
      <div ref="mapContainer" class="w-full h-full"></div>
      <button @click="moveToMyLocation" 
              class="absolute bottom-10 right-10 z-20 btn btn-circle bg-white border-none shadow-xl hover:bg-slate-50">
        📍
      </button>
    </main>
  </div>
</template>