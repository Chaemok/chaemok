<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import api from '@/api'; 
import { staticData } from '@/constants/mapData';

// ==========================================
// 1. 상태 변수 (기능용)
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

// ==========================================
// 2. 추가된 디자인용 변수 (로직 영향 X)
// ==========================================
const userMarker = ref(null);   // 현위치 빨간 마커
const isGpsActive = ref(false); // GPS 배지 상태

const searchTypes = [
  { value: 'BANK', label: '은행' },
  { value: 'SEC', label: '증권사' },
  { value: 'ATM', label: 'ATM' }
];

const selectedSido = ref('');
const selectedGugun = ref('');
const selectedType = ref('BANK'); 
const selectedBank = ref('ALL_BANK'); 
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
// 3. 지도 로직 (네가 준 원본 코드 100%)
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
      // 🐜 [디자인] 인포윈도우 내용만 예쁘게 수정 (기능 영향 없음)
      infowindow.value.setContent(`
        <div style="padding:10px; min-width:150px; background:white; border-radius:12px; border:none;">
          <div style="font-weight:900; font-size:14px; color:#1e293b; margin-bottom:4px;">${place.name}</div>
          <div style="font-size:11px; color:#64748b;">${place.address}</div>
        </div>
      `);
      infowindow.value.open(map.value, marker);
    });
  });
  map.value.setBounds(bounds);
};

const initMap = () => {
  if (!window.kakao || !mapContainer.value) return;
  window.kakao.maps.load(() => {
    const options = { center: new window.kakao.maps.LatLng(37.5215, 126.9243), level: 4 };
    map.value = new window.kakao.maps.Map(mapContainer.value, options);
    geocoder.value = new window.kakao.maps.services.Geocoder();
    infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 20 });
    moveToMyLocation();
  });
};

// 🐜 [추가] 빨간색 현위치 마커 함수 (단독 실행)
const setUserMarker = (loc) => {
  if (userMarker.value) userMarker.value.setMap(null);
  // SVG 마커 사용 (이미지 깨짐 방지)
  const svgMarker = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48">
      <path fill="#EF4444" stroke="#FFFFFF" stroke-width="1.5" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
      <circle cx="12" cy="9" r="2.5" fill="white"/>
    </svg>`;
  const imageSrc = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgMarker);
  const imageSize = new window.kakao.maps.Size(40, 40);
  const markerImage = new window.kakao.maps.MarkerImage(imageSrc, imageSize);
  
  userMarker.value = new window.kakao.maps.Marker({ position: loc, image: markerImage, zIndex: 30 });
  userMarker.value.setMap(map.value);
};

const moveToMyLocation = () => {
  if (navigator.geolocation && map.value) {
    navigator.geolocation.getCurrentPosition((pos) => {
      const lat = pos.coords.latitude; const lng = pos.coords.longitude;
      userLocation.value = { lat, lng };
      
      // 🐜 [상태 업데이트]
      isGpsActive.value = true;
      
      const loc = new window.kakao.maps.LatLng(lat, lng);
      map.value.setCenter(loc);
      locationBias.value = `${lat},${lng}`;
      
      // 🐜 [마커 찍기]
      setUserMarker(loc);
      
    }, (err) => {
      isGpsActive.value = false;
      console.warn("GPS 접근 거부");
    }, { enableHighAccuracy: true, timeout: 5000 });
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
    
    polyline.value = new window.kakao.maps.Polyline({ 
      path: linePath, strokeWeight: 6, strokeColor: '#2563EB', strokeOpacity: 0.8, lineJoin: 'round' 
    });
    polyline.value.setMap(map.value);
    const bounds = new window.kakao.maps.LatLngBounds();
    linePath.forEach(p => bounds.extend(p));
    map.value.setBounds(bounds);
  } catch (err) { alert("경로를 불러올 수 없습니다."); }
};

// ==========================================
// 4. 검색 실행 (네가 준 원본 그대로)
// ==========================================
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
    if (userLocation.value) locationBias.value = `${userLocation.value.lat},${userLocation.value.lng}`;
    searchPlacesApi(query);
  }
};

const searchPlacesApi = async (query) => {
  if (!locationBias.value || locationBias.value === ',') locationBias.value = '37.5215,126.9243';
  const [lat, lng] = locationBias.value.split(',');
  
  try {
    const res = await api.get('map/map-search/', { params: { query, lat, lng } });
    if (res.data?.documents) {
      let filtered = res.data.documents;
      if (selectedType.value === 'BANK') {
        filtered = filtered.filter(p => !p.place_name.includes('365') && !p.place_name.includes('ATM') && !p.place_name.includes('무인') && !p.place_name.includes('주차장'));
      }
      placesData.value = filtered.map(p => ({
        id: p.id, name: p.place_name, address: p.address_name, x: p.x, y: p.y, distance: p.distance
      }));
      displayPlaces(placesData.value);
    }
  } catch (error) { 
    alert("검색 결과를 불러올 수 없습니다.");
  } finally { loading.value = false; }
};

onMounted(() => initMap());
</script>

<template>
  <div class="flex h-[calc(100vh-80px)] w-full overflow-hidden bg-slate-50 font-pretendard">
    <aside class="w-[420px] bg-white border-r border-slate-100 flex flex-col shadow-2xl z-10">
      <div class="p-8 space-y-6 border-b border-slate-50">
        <div class="flex items-center justify-between">
          <div class="flex flex-col">
            <h2 class="text-2xl font-black text-slate-900 tracking-tighter italic leading-none">Smart Ants Map</h2>
            <span class="text-[10px] text-slate-300 font-bold mt-1 tracking-widest uppercase">Financial Intelligence</span>
          </div>
          <div :class="isGpsActive ? 'bg-emerald-50 text-emerald-600 border-emerald-100' : 'bg-slate-100 text-slate-400 border-slate-200'"
               class="flex items-center gap-1.5 px-3 py-1.5 rounded-full border transition-all duration-500">
            <div :class="isGpsActive ? 'bg-emerald-500 animate-pulse' : 'bg-slate-300'" class="w-1.5 h-1.5 rounded-full"></div>
            <span class="text-[9px] font-black tracking-widest uppercase">{{ isGpsActive ? 'GPS Active' : 'GPS Offline' }}</span>
          </div>
        </div>
        
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-2">
            <select v-model="selectedSido" class="select select-bordered rounded-2xl select-sm focus:border-blue-500 bg-slate-50 border-none font-bold text-xs shadow-inner">
              <option value="">전국 단위</option>
              <option v-for="(_, sido) in staticData.koreaAreas" :key="sido" :value="sido">{{ sido }}</option>
            </select>
            <select v-model="selectedGugun" class="select select-bordered rounded-2xl select-sm focus:border-blue-500 bg-slate-50 border-none font-bold text-xs shadow-inner">
              <option value="">구/군 전체</option>
              <option v-for="gugun in gugunOptions" :key="gugun" :value="gugun">{{ gugun }}</option>
            </select>
          </div>
          
          <div class="flex bg-slate-100 p-1.5 rounded-2xl">
            <button v-for="t in searchTypes" :key="t.value" @click="selectedType = t.value"
                    :class="selectedType === t.value ? 'bg-white text-blue-600 shadow-md scale-[1.02]' : 'text-slate-400'"
                    class="flex-1 py-2.5 text-[12px] font-black rounded-xl transition-all duration-300">
              {{ t.label }}
            </button>
          </div>
          
          <div class="flex gap-2">
            <select v-model="selectedBank" class="select select-bordered rounded-2xl select-sm flex-1 focus:border-blue-500 bg-slate-50 border-none font-bold text-xs shadow-inner">
              <option v-for="opt in bankOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
            </select>
            <button @click="executeSearch" class="btn bg-blue-600 hover:bg-blue-700 text-white border-none btn-sm rounded-2xl px-6 shadow-lg transition-all active:scale-95" :disabled="loading">
              <span v-if="loading" class="loading loading-spinner loading-xs"></span>
              <span v-else class="font-black text-xs uppercase tracking-wider">Search</span>
            </button>
          </div>
        </div>
      </div>

      <div class="flex-1 overflow-y-auto p-6 space-y-5 no-scrollbar">
        <div v-if="placesData.length === 0 && !loading" class="flex flex-col items-center justify-center py-28 px-10 text-center animate-fade-in">
          <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-6 text-4xl grayscale opacity-30">🐜</div>
          <h3 class="text-lg font-black text-slate-800 mb-1 tracking-tight">검색 결과가 없습니다</h3>
          <p class="text-[13px] text-slate-400 font-medium leading-relaxed italic">
            지도를 움직이거나 필터를 변경하여<br/>주변 금융 기관을 찾아보세요.
          </p>
        </div>
        
        <div v-for="place in placesData" :key="place.id" 
             class="group relative bg-white p-6 rounded-[2.5rem] border border-slate-100 hover:border-blue-500 hover:shadow-[0_25px_50px_-12px_rgba(37,99,235,0.12)] transition-all duration-300 cursor-pointer">
          <div class="flex justify-between items-start mb-4">
            <div class="flex-1">
              <span class="inline-block px-2.5 py-1 rounded-lg bg-blue-50 text-blue-600 text-[10px] font-black mb-2 tracking-tighter uppercase">
                {{ searchTypes.find(t => t.value === selectedType)?.label }} 지점
              </span>
              <h4 class="text-[17px] font-black text-slate-800 leading-tight group-hover:text-blue-600 transition-colors">
                {{ place.name }}
              </h4>
            </div>
            <button @click.stop="map.panTo(new window.kakao.maps.LatLng(place.y, place.x))" 
                    class="p-3 hover:bg-blue-50 rounded-2xl transition-all group/loc shadow-sm border border-slate-50 bg-white group-hover:border-blue-100">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5 text-slate-300 group-hover/loc:text-blue-600 transition-colors">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
              </svg>
            </button>
          </div>
          <p class="text-[13px] text-slate-400 font-medium mb-6 line-clamp-1 italic">{{ place.address }}</p>
          <div class="flex items-center justify-between border-t border-slate-50 pt-5">
            <div class="flex items-center gap-2 text-blue-600">
              <div class="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></div>
              <span class="text-[12px] font-black italic tracking-tighter">{{ place.distance }}m</span>
            </div>
            <button @click.stop="drawRoute(place)" class="flex items-center gap-2 bg-slate-950 text-white px-6 py-3 rounded-2xl text-[12px] font-black hover:bg-blue-600 transition-all shadow-xl group/route active:scale-95">
              <span>길찾기</span><span class="group-hover/route:animate-bounce-x">🚀</span>
            </button>
          </div>
        </div>
      </div>
    </aside>

    <main class="flex-1 relative">
      <div ref="mapContainer" class="w-full h-full bg-slate-100"></div>
      
      <button @click="moveToMyLocation" 
              class="absolute bottom-10 right-10 z-20 w-16 h-16 bg-white rounded-3xl shadow-2xl flex items-center justify-center hover:bg-blue-600 hover:text-white active:scale-90 transition-all border border-slate-100 text-2xl shadow-blue-200/40 group">
        <span class="group-hover:animate-bounce">📍</span>
      </button>
    </main>
  </div>
</template>

<style scoped>
.font-pretendard { font-family: 'Pretendard Variable', 'Pretendard', sans-serif; }
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
@keyframes bounce-x { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(5px); } }
.group-hover\/route\:animate-bounce-x { animation: bounce-x 0.6s infinite; }
.animate-fade-in { animation: fadeIn 0.6s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>