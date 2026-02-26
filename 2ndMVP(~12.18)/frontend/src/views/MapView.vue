<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';
import { useFinanceStore } from '@/stores/finance';
import BaseCard from '@/components/BaseCard.vue'; // 경로 확인 필요

const financeStore = useFinanceStore();

// ==========================================
// 🚨 [필수 설정] 카카오 앱 키 (사용자님의 키로 교체 필요)
// ==========================================
const KAKAO_MAP_JS_KEY = '23fbca3b74e77ccdfc30b0024a5256cf'

// ==========================================
// DTL에서 가져온 정적 데이터
// ==========================================
const staticData = {
  "koreaAreas": {
    "서울": ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"],
    "경기": [
      "수원시 장안구", "수원시 권선구", "수원시 팔달구", "수원시 영통구",
      "성남시 수정구", "성남시 중원구", "성남시 분당구",
      "의정부시", "안양시 만안구", "안양시 동안구", "부천시", "광명시", "평택시", "동두천시",
      "안산시 상록구", "안산시 단원구", "고양시 덕양구", "고양시 일산동구", "고양시 일산서구",
      "과천시", "구리시", "남양주시", "오산시", "시흥시", "군포시", "의왕시", "하남시",
      "용인시 처인구", "용인시 기흥구", "용인시 수지구",
      "파주시", "이천시", "안성시", "김포시", "화성시", "광주시", "양주시", "포천시", "여주시",
      "연천군", "가평군", "양평군"
    ],
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
    "경북": ["포항시 남구", "포항시 북구", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시", "상주시", "문경시", "경산시", "군위군", "의성군", "청송군", "영양군", "영덕군", "청도군", "고령군", "성주군", "칠곡군", "예천군", "봉화군", "울진군", "울릉군"],
    "경남": ["창원시 의창구", "창원시 성산구", "창원시 마산합포구", "창원시 마산회원구", "창원시 진해구", "진주시", "통영시", "사천시", "김해시", "밀양시", "거제시", "양산시", "의령군", "함안군", "창녕군", "고성군", "남해군", "하동군", "산청군", "함양군", "거창군", "합천군"],
    "전북": ["전주시 완산구", "전주시 덕진구", "군산시", "익산시", "정읍시", "남원시", "김제시", "완주군", "진안군", "무주군", "장수군", "임실군", "순창군", "고창군", "부안군"],
    "전남": ["목포시", "여수시", "순천시", "나주시", "광양시", "담양군", "곡성군", "구례군", "고흥군", "보성군", "화순군", "장흥군", "강진군", "해남군", "영암군", "무안군", "함평군", "영광군", "장성군", "완도군", "진도군", "신안군"],
    "제주": ["제주시", "서귀포시"]
  },
  "financialInstitutions": [
    { "name": "KB국민은행", "type": "BANK" },
    { "name": "신한은행", "type": "BANK" },
    { "name": "우리은행", "type": "BANK" },
    { "name": "하나은행", "type": "BANK" },
    { "name": "NH농협은행", "type": "BANK" },
    { "name": "IBK기업은행", "type": "BANK" },
    { "name": "SC제일은행", "type": "BANK" },
    { "name": "한국씨티은행", "type": "BANK" },
    { "name": "iM뱅크(대구은행)", "type": "BANK" },
    { "name": "부산은행", "type": "BANK" },
    { "name": "경남은행", "type": "BANK" },
    { "name": "광주은행", "type": "BANK" },
    { "name": "전북은행", "type": "BANK" },
    { "name": "제주은행", "type": "BANK" },
    { "name": "우체국", "type": "BANK" },
    { "name": "새마을금고", "type": "BANK" },
    { "name": "신협", "type": "BANK" },
    { "name": "수협은행", "type": "BANK" },
    { "name": "저축은행", "type": "BANK" },
    { "name": "키움증권", "type": "SEC" },
    { "name": "미래에셋증권", "type": "SEC" },
    { "name": "삼성증권", "type": "SEC" },
    { "name": "한국투자증권", "type": "SEC" },
    { "name": "NH투자증권", "type": "SEC" },
    { "name": "KB증권", "type": "SEC" },
    { "name": "신한투자증권", "type": "SEC" },
    { "name": "대신증권", "type": "SEC" },
    { "name": "하나증권", "type": "SEC" },
    { "name": "메리츠증권", "type": "SEC" },
    { "name": "유안타증권", "type": "SEC" },
    { "name": "유진투자증권", "type": "SEC" },
    { "name": "한화투자증권", "type": "SEC" },
    { "name": "현대차증권", "type": "SEC" },
    { "name": "DB금융투자", "type": "SEC" },
    { "name": "교보증권", "type": "SEC" },
    { "name": "하이투자증권", "type": "SEC" },
    { "name": "SK증권", "type": "SEC" },
    { "name": "신영증권", "type": "SEC" },
    { "name": "이베스트투자증권", "type": "SEC" }
  ]
};

// ==========================================
// 지도 및 검색 상태
// ==========================================
const mapContainer = ref(null); 
const map = ref(null);
const geocoder = ref(null); // 지역 주소를 좌표로 변환하기 위함
const infowindow = ref(null);
const markers = ref([]);
const kakao = window.kakao;

const loading = ref(false);
const placesData = ref([]);

// 필터 상태
const selectedSido = ref('');
const selectedGugun = ref('');
const selectedType = ref('BANK'); // BANK, SEC, ATM
const selectedBank = ref('ALL_BANK'); 

// Kakao Maps에서 사용될 위치 참조 (DTL의 location_bias 역할)
const locationBias = ref('MY_LOCATION'); 

// ==========================================
// Computed & Watch (필터 로직)
// ==========================================

// 시/군/구 드롭다운 옵션
const gugunOptions = computed(() => {
    return selectedSido.value ? staticData.koreaAreas[selectedSido.value] : [];
});

// 금융기관 드롭다운 옵션
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

// 시/도 변경 시 구/군 초기화
watch(selectedSido, () => {
    selectedGugun.value = '';
});

// 구분 변경 시 금융기관 초기화
watch(selectedType, () => {
    selectedBank.value = bankOptions.value[0]?.value || '';
});

// ==========================================
// 지도 기능 함수 (DTL JS 로직 변환)
// ==========================================

const clearMarkers = () => {
    markers.value.forEach(m => m.setMap(null));
    markers.value = [];
};

const displayPlaces = (places) => {
    clearMarkers();
    if (!map.value || places.length === 0) return;

    const bounds = new kakao.maps.LatLngBounds();

    places.forEach((place) => {
        // 🚨 [주의] 백엔드 API가 lat/lng 또는 y/x를 반환해야 합니다.
        // 현재는 'y'와 'x' (위도/경도)가 포함된 DTL 구조를 가정합니다.
        const pos = new kakao.maps.LatLng(place.y, place.x); 
        
        const marker = new kakao.maps.Marker({
            map: map.value,
            position: pos,
            title: place.name
        });
        markers.value.push(marker);
        bounds.extend(pos);

        // 마커 클릭 이벤트: 인포윈도우 표시
        kakao.maps.event.addListener(marker, 'click', function() {
            map.value.panTo(pos);
            const content = `<div style="padding:5px;font-size:12px;"><strong>${place.name}</strong></div>`;
            infowindow.value.setContent(content);
            infowindow.value.open(map.value, marker);
        });
    });

    map.value.setBounds(bounds);
};


const initMap = () => {
    if (!kakao || !mapContainer.value) return;
    
    const options = {
        center: new kakao.maps.LatLng(37.5665, 126.9780), // 서울 시청
        level: 4
    };
    map.value = new kakao.maps.Map(mapContainer.value, options);
    geocoder.value = new kakao.maps.services.Geocoder(); // geocoding 서비스
    infowindow.value = new kakao.maps.InfoWindow({ zIndex: 1 });
    
    moveToMyLocation();
};

const moveToMyLocation = () => {
    if (navigator.geolocation && map.value) {
        navigator.geolocation.getCurrentPosition((pos) => {
            const loc = new kakao.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
            map.value.setCenter(loc);
            map.value.setLevel(4);
            
            // locationBias 업데이트 (검색 시 현위치 기준 사용)
            locationBias.value = `${pos.coords.latitude},${pos.coords.longitude}`;
        }, (err) => {
            alert("위치 정보를 가져올 수 없습니다. 기본 위치(서울)에서 검색합니다.");
        });
    }
};

// ----------------------------------------------------
// 🚨 [핵심] 검색어 및 위치를 결정하고 API 호출
// ----------------------------------------------------

const executeSearch = () => {
    clearMarkers();
    placesData.value = []; 
    
    const typeVal = selectedType.value;
    const bankVal = selectedBank.value;
    const sidoVal = selectedSido.value;
    const gugunVal = selectedGugun.value;

    // 1. 검색어 결정 (Query)
    let finalQuery = '';
    if (typeVal === 'ATM') {
        finalQuery = 'ATM';
    } else if (bankVal.startsWith('ALL')) {
        finalQuery = typeVal === 'BANK' ? '은행' : '증권사';
    } else {
        finalQuery = bankVal;
    }
    
    // 2. 위치 결정 및 지오코딩 (Location Bias)
    // 시/도나 구/군이 선택된 경우, 해당 주소로 지도를 이동하고 검색을 시작합니다.
    if (sidoVal) {
        let address = sidoVal + (gugunVal ? ' ' + gugunVal : '');

        geocoder.value.addressSearch(address, function(result, status) {
            if (status === kakao.maps.services.Status.OK && result[0]) {
                const coords = new kakao.maps.LatLng(result[0].y, result[0].x);
                map.value.setCenter(coords);
                
                // 검색 좌표 업데이트
                locationBias.value = `${result[0].y},${result[0].x}`;

                // 지오코딩 성공 후 API 호출
                searchPlacesApi(finalQuery);
            } else {
                alert("지역 주소를 찾을 수 없습니다.");
            }
        });
    } else {
        // 지역 선택이 없으면, 현재 맵 중앙 기준 (moveToMyLocation에서 설정된 locationBias 사용)
        searchPlacesApi(finalQuery);
    }
};


const searchPlacesApi = async (query) => {
    loading.value = true;
    
    // console.log("최종 검색 요청:", query, "@", locationBias.value);

    try {
        const response = await axios.get(`${financeStore.API_URL}/api/finances/maps/search/`, {
            params: {
                query: query,
                location_bias: locationBias.value,
            }
        });

        if (response.data.success && response.data.places) {
            placesData.value = response.data.places;
            displayPlaces(placesData.value); // 지도에 표시
            
        } else {
            console.error('검색 실패 또는 결과 없음:', response.data.error || '알 수 없는 오류');
        }

    } catch (error) {
        console.error('API 호출 중 오류 발생:', error);
    } finally {
        loading.value = false;
    }
};

// ==========================================
// 라이프사이클 및 SDK 로드
// ==========================================

// onMounted(() => {
//     // 1. Kakao Map SDK 동적 로드
//     const script = document.createElement('script');
    
//     // ✨ [핵심 수정] URL을 명시적으로 'https:'로 시작하도록 변경
//     script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_MAP_JS_KEY}&libraries=services&autoload=false`;
    
//     script.onload = () => {
//         // 2. 로드 완료 후 지도 초기화
//         // autoload=false 옵션을 사용하셨다면, 이 로직은 반드시 필요합니다.
//         if (window.kakao && kakao.maps) {
//              kakao.maps.load(initMap);
//         } else {
//              console.error("Kakao Map 객체 로드 실패.");
//         }
//     };
//     document.head.appendChild(script);
// });
</script>

<!-- <template>
    <div class="max-w-7xl mx-auto px-4 py-10 min-h-screen">
        <h2 class="text-3xl font-bold mb-8">🗺️ 은행 / 증권사 / ATM 찾기</h2>

        <BaseCard class="mb-6 p-6 bg-gray-50 border border-gray-100">
            <div class="flex gap-3 flex-wrap items-end">
                
                <div style="flex:1; min-width: 120px;">
                    <label class="block text-sm font-medium text-gray-600 mb-1">광역시 / 도</label>
                    <select v-model="selectedSido" class="select select-bordered w-full h-10 min-h-0 text-sm">
                        <option value="">전체</option>
                        <option v-for="(guguns, sido) in staticData.koreaAreas" :key="sido" :value="sido">{{ sido }}</option>
                    </select>
                </div>
                
                <div style="flex:1; min-width: 120px;">
                    <label class="block text-sm font-medium text-gray-600 mb-1">시 / 군 / 구</label>
                    <select v-model="selectedGugun" class="select select-bordered w-full h-10 min-h-0 text-sm" :disabled="!selectedSido">
                        <option value="">전체</option>
                        <option v-for="gugun in gugunOptions" :key="gugun" :value="gugun">{{ gugun }}</option>
                    </select>
                </div>

                <div style="flex:0.8; min-width: 110px;">
                    <label class="block text-sm font-medium text-gray-600 mb-1">구분</label>
                    <select v-model="selectedType" @change="handleTypeChange" class="select select-bordered w-full h-10 min-h-0 text-sm">
                        <option value="BANK">은행</option>
                        <option value="SEC">증권사</option>
                        <option value="ATM">ATM (365코너)</option>
                    </select>
                </div>

                <div style="flex:1.2; min-width: 140px;">
                    <label class="block text-sm font-medium text-gray-600 mb-1">금융기관 선택</label>
                    <select v-model="selectedBank" class="select select-bordered w-full h-10 min-h-0 text-sm">
                        <option v-for="opt in bankOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                    </select>
                </div>
                
                <button @click="executeSearch" class="btn btn-primary" :disabled="loading" style="height: 40px; padding: 0 20px;">
                    <span v-if="loading" class="loading loading-spinner"></span>
                    <span v-else>🔍 검색</span>
                </button>

                <button @click="moveToMyLocation" class="btn btn-ghost border border-gray-300" style="height: 40px; padding: 0 15px;">
                    📍 내 위치로 이동
                </button>
            </div>
        </BaseCard>

        <div class="split-container" style="display: flex; gap: 20px; height: 600px;">
            <div ref="mapContainer" id="map-container" style="flex: 7; height: 100%; border-radius: 12px; border: 1px solid #ddd; position: relative;">
                <div v-if="loading" class="absolute inset-0 bg-white/70 flex items-center justify-center z-10" style="border-radius: 12px;">
                    <span class="loading loading-spinner loading-lg text-primary"></span>
                </div>
                <div v-if="!map" class="w-full h-full flex items-center justify-center text-gray-500">
                    지도 로딩 중...
                </div>
            </div>

            <div class="result-wrapper bg-white shadow-md" style="flex: 3; height: 100%; display: flex; flex-direction: column; border: 1px solid #eee; border-radius: 12px;">
                <div class="result-header" style="padding: 15px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; background: #fdfdfd; border-radius: 12px 12px 0 0;">
                    <h3 class="result-title" style="margin:0; font-size: 16px; font-weight: bold;">검색 결과</h3>
                    <span class="result-count" style="color:#007bff; font-weight:bold;">{{ placesData.length }}건</span>
                </div>
                <ul id="result-list" class="result-list" style="list-style:none; padding:0; margin:0; overflow-y:auto; flex: 1;">
                    <li v-if="placesData.length === 0 && !loading" style="padding:40px 0; text-align:center; color:#888;">
                        <div style="font-size:30px; margin-bottom:10px;">🗺️</div>
                        검색 버튼을 눌러 주변 장소를 찾아보세요.
                    </li>
                    <li v-for="(place, index) in placesData" :key="place.id" 
                        style="padding:15px; border-bottom:1px solid #eee; cursor:pointer; hover:bg-gray-50"
                        @click="map.panTo(new kakao.maps.LatLng(place.y, place.x))"
                    >
                        <div style="font-weight:bold; font-size:14px; margin-bottom:4px;">{{ index + 1 }}. {{ place.name }}</div>
                        <div style="font-size:12px; color:#666;">{{ place.address }}</div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template> -->
<template>
    <div ref="mapContainer" id="map-container" style="...생략...">
        <div v-if="!map" class="w-full h-full flex items-center justify-center text-gray-500">
            현재 지도 서비스는 고치고 있습니다. 🛠️
        </div>
    </div>
</template>