# backend/maps/views.py


from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
import requests # 외부 API 통신을 위해 필요
import traceback
import os

# 🚨 [필수 설정] 카카오 REST API 키 (Settings.py나 환경 변수에서 가져옴)
# settings.py에 KAKAO_REST_API_KEY를 정의하고 가져오는 것을 권장합니다.
KAKAO_REST_API_KEY = '676d89680b40b5e9fa41b47be77242ab'
KAKAO_API_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def map_search_places(request):
    query = request.GET.get('query', '은행') 
    location_bias = request.GET.get('location_bias') # (lat,lng 형태)

    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
    params = {
        'query': query,
        'sort': 'distance', # 거리순 정렬
        'radius': 20000, # 최대 20km 반경
    }
    
    # location_bias (사용자 위치)가 있다면, x, y에 위경도 파싱하여 추가
    if location_bias and location_bias != 'MY_LOCATION':
        try:
            # location_bias가 "위도,경도" 형태로 온다고 가정
            lat, lng = map(float, location_bias.split(','))
            params['x'] = lng # 카카오 API는 x(경도), y(위도) 순서
            params['y'] = lat
        except ValueError:
            pass # 파싱 오류 시 위치 기반 검색 포기

    try:
        # 1. 카카오 API 호출
        response = requests.get(KAKAO_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # 2. Vue/Kakao Map이 요구하는 구조로 데이터 정제
        places_data = []
        for place in data.get('documents', []):
            places_data.append({
                'id': place.get('id'),
                'name': place.get('place_name'),
                'address': place.get('road_address_name') or place.get('address_name'),
                # 카카오 API는 x(경도), y(위도)를 직접 반환함. Vue는 x, y로 사용
                'y': float(place.get('y')), # 위도
                'x': float(place.get('x'))  # 경도
            })
        
        print(f"✅ 카카오 API 검색 결과: {len(places_data)}개 장소 반환.")
        return JsonResponse({'success': True, 'places': places_data})

    except requests.exceptions.HTTPError as http_err:
        print(f"🔥 카카오 API 오류: {http_err} - 응답: {response.text}")
        return JsonResponse({'success': False, 'error': '카카오 API 호출 오류'}, status=response.status_code)
    except Exception as e:
        print(f"🔥 [Error] Map Search Failed: {e}")
        return JsonResponse({'success': False, 'error': '지도 검색 중 오류가 발생했습니다.'}, status=500)
