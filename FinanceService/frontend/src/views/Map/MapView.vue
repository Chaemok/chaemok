<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import api from '@/api'; 
import { staticData } from '@/constants/mapData';

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
const polyline = ref(null); 
const userLocation = ref(null); 

// 필터 상태
const selectedSido = ref('');
const selectedGugun = ref('');
const selectedType = ref('BANK'); 
const selectedBank = ref('ALL_BANK'); 

// 🐜 [수정] 기본 위치를 '여의도역' 좌표로 설정
// 여의도역 좌표: 위도 37.5215, 경도 126.9243
const locationBias = ref('37.5215,126.9243'); 

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
const clearMarkers = () => { markers.value.forEach(m => m.setMap(null)); markers.value = []; };

const displayPlaces = (places) => {
  clearMarkers();
  if (!map.value || places.length === 0) return;
  const bounds = new window.kakao.maps.LatLngBounds();
  places.forEach((place) => {
    const pos = new window.kakao.maps.LatLng(place.y, place.x); 
    const marker = new window.kakao.maps.Marker({ map: map.value, position: pos });
    markers.value.push(marker);
    bounds.extend(pos);
    window.kakao.maps.event.addListener(marker, 'click', () => {
      map.value.panTo(pos);
      infowindow.value.setContent(`<div class="p-2 text-xs font-bold text-slate-800">${place.name}</div>`);
      infowindow.value.open(map.value, marker);
    });
  });
  map.value.setBounds(bounds);
};

const initMap = () => {
  if (!window.kakao || !mapContainer.value) return;
  window.kakao.maps.load(() => {
    // 🐜 시작 시 여의도역을 중심으로 지도 생성
    const options = { center: new window.kakao.maps.LatLng(37.5215, 126.9243), level: 4 };
    map.value = new window.kakao.maps.Map(mapContainer.value, options);
    geocoder.value = new window.kakao.maps.services.Geocoder();
    infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 1 });
    
    // 지도 생성 후 즉시 내 위치 찾기 시도
    moveToMyLocation();
  });
};

// 🐜 내 위치(GPS) 사용 로직 강화
const moveToMyLocation = () => {
  if (navigator.geolocation && map.value) {
    navigator.geolocation.getCurrentPosition((pos) => {
      const lat = pos.coords.latitude;
      const lng = pos.coords.longitude;
      userLocation.value = { lat, lng };
      
      const loc = new window.kakao.maps.LatLng(lat, lng);
      map.value.setCenter(loc);
      // 검색 기준점도 내 위치로 즉시 업데이트
      locationBias.value = `${lat},${lng}`;
      console.log("🐜 내 위치 확인 완료:", lat, lng);
    }, (err) => {
      console.warn("GPS 접근 거부 또는 오류. 기본 위치(여의도역)를 유지합니다.");
    }, {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0
    });
  }
};

const drawRoute = async (place) => {
  if (!userLocation.value) { alert("내 위치를 먼저 잡아주세요! 📍"); moveToMyLocation(); return; }
  try {
    const origin = `${userLocation.value.lng},${userLocation.value.lat}`;
    const destination = `${place.x},${place.y}`;
    const res = await api.get('map/route/', { params: { origin, destination } });
    if (polyline.value) polyline.value.setMap(null);
    const linePath = res.data.path.map(p => new window.kakao.maps.LatLng(p.lat, p.lng));
    polyline.value = new window.kakao.maps.Polyline({ path: linePath, strokeWeight: 5, strokeColor: '#1e3a8a', strokeOpacity: 0.8 });
    polyline.value.setMap(map.value);
    const bounds = new window.kakao.maps.LatLngBounds();
    linePath.forEach(p => bounds.extend(p));
    map.value.setBounds(bounds);
  } catch (err) { alert("경로를 불러올 수 없습니다. 🐜"); }
};

const executeSearch = () => {
  loading.value = true;
  let query = selectedBank.value.startsWith('ALL') ? (selectedType.value === 'BANK' ? '은행' : selectedType.value === 'SEC' ? '증권사' : 'ATM') : selectedBank.value;
  
  if (selectedSido.value) {
    const address = selectedSido.value + (selectedGugun.value ? ' ' + selectedGugun.value : '');
    geocoder.value.addressSearch(address, (result, status) => {
      if (status === window.kakao.maps.services.Status.OK) {
        locationBias.value = `${result[0].y},${result[0].x}`;
        searchPlacesApi(query);
      }
    });
  } else {
    // 🐜 지역 선택이 없을 땐 GPS 위치를 우선으로, 없으면 여의도(기본값) 사용
    if (userLocation.value) {
      locationBias.value = `${userLocation.value.lat},${userLocation.value.lng}`;
    }
    searchPlacesApi(query);
  }
};

const searchPlacesApi = async (query) => {
  // 🐜 좌표 누락 방지 안전장치
  if (!locationBias.value || locationBias.value === ',') {
    locationBias.value = '37.5215,126.9243'; // 최후의 수단: 여의도역
  }

  const [lat, lng] = locationBias.value.split(',');
  
  try {
    const res = await api.get('map/map-search/', { params: { query, lat, lng } });
    if (res.data?.documents) {
      let filtered = res.data.documents;
      if (selectedType.value === 'BANK') {
        filtered = filtered.filter(p => !p.place_name.includes('365') && !p.place_name.includes('ATM'));
      }
      placesData.value = filtered.map(p => ({
        id: p.id, name: p.place_name, address: p.address_name, x: p.x, y: p.y, distance: p.distance
      }));
      displayPlaces(placesData.value);
    }
  } catch (error) { 
    console.error('검색 실패:', error);
    alert("검색 결과를 불러올 수 없습니다.");
  } finally { 
    loading.value = false; 
  }
};

onMounted(() => initMap());
</script>

<template>
  <div class="flex h-[calc(100vh-80px)] w-full overflow-hidden bg-slate-50 font-sans">
    <aside class="w-[420px] bg-white border-r border-slate-100 flex flex-col shadow-xl z-10">
      <div class="p-6 space-y-6 border-b border-slate-50">
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-black text-slate-800 tracking-tight italic">Smart Ants Map 📍</h2>
          <div class="flex items-center gap-1">
            <span v-if="userLocation" class="text-[9px] bg-emerald-50 text-emerald-600 px-2 py-1 rounded-lg font-black tracking-widest">GPS ON</span>
            <span v-else class="text-[9px] bg-slate-100 text-slate-400 px-2 py-1 rounded-lg font-black tracking-widest">DEFAULT: YEOUIDO</span>
          </div>
        </div>
        
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-2">
            <select v-model="selectedSido" class="select select-bordered rounded-xl select-sm focus:border-primary">
              <option value="">전체 (내 위치 기준)</option>
              <option v-for="(_, sido) in staticData.koreaAreas" :key="sido" :value="sido">{{ sido }}</option>
            </select>
            <select v-model="selectedGugun" class="select select-bordered rounded-xl select-sm focus:border-primary">
              <option value="">구/군 선택</option>
              <option v-for="gugun in gugunOptions" :key="gugun" :value="gugun">{{ gugun }}</option>
            </select>
          </div>
          <div class="flex bg-slate-100 p-1 rounded-xl">
            <button v-for="t in ['BANK', 'SEC', 'ATM']" :key="t" @click="selectedType = t"
                    :class="selectedType === t ? 'bg-white text-primary shadow-sm' : 'text-slate-400'"
                    class="flex-1 py-1.5 text-[11px] font-black rounded-lg transition-all">{{ t }}</button>
          </div>
          <div class="flex gap-2">
            <select v-model="selectedBank" class="select select-bordered rounded-xl select-sm flex-1 focus:border-primary">
              <option v-for="opt in bankOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
            </select>
            <button @click="executeSearch" class="btn btn-primary btn-sm rounded-xl px-6" :disabled="loading">
              <span v-if="loading" class="loading loading-spinner loading-xs"></span>
              <span v-else class="font-black">검색</span>
            </button>
          </div>
        </div>
      </div>

      <div class="flex-1 overflow-y-auto p-6 space-y-4">
        <div v-if="placesData.length === 0 && !loading" class="text-center py-20 text-slate-300">
          <p class="text-4xl mb-2">🐜</p>
          <p class="text-[10px] font-black uppercase tracking-[0.2em]">Financial Intelligence</p>
        </div>
        <div v-for="place in placesData" :key="place.id" class="card border border-slate-100 p-5 rounded-[1.8rem] hover:border-primary hover:shadow-lg transition-all bg-white group">
          <p class="text-[10px] font-black text-primary mb-1 tracking-widest uppercase">{{ selectedType }}</p>
          <h4 class="font-bold text-slate-800 group-hover:text-primary transition-colors">{{ place.name }}</h4>
          <p class="text-[11px] text-slate-400 mt-2 font-medium">{{ place.address }}</p>
          <div class="flex justify-between items-center mt-5">
            <span class="text-[10px] font-black text-slate-300 italic">{{ place.distance }}m</span>
            <div class="flex gap-1">
              <button @click.stop="map.panTo(new window.kakao.maps.LatLng(place.y, place.x))" class="btn btn-xs btn-ghost text-slate-400 font-bold">위치</button>
              <button @click.stop="drawRoute(place)" class="btn btn-xs bg-blue-950 text-white border-none hover:bg-black rounded-lg px-4">길찾기 🚀</button>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <main class="flex-1 relative">
      <div ref="mapContainer" class="w-full h-full bg-slate-100"></div>
      <button @click="moveToMyLocation" class="absolute bottom-10 right-10 z-20 btn btn-circle btn-lg bg-white border-none shadow-2xl hover:bg-slate-50 active:scale-90 transition-all">📍</button>
    </main>
  </div>
</template>