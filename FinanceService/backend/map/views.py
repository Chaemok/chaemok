# map/views.py 전체 코드
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view

# 🐜 카카오 REST API 키
KAKAO_REST_KEY = '676d89680b40b5e9fa41b47be77242ab'

@api_view(['GET'])
def map_search(request):
    """주변 금융기관 검색 (카카오 규격 15개 제한 적용)"""
    query = request.GET.get('query')
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_KEY}"}
    
    params = {
        "query": query,
        "x": lng,
        "y": lat,
        "radius": 20000, 
        # 🐜 [수정] 카카오 API 최대 허용치인 15로 변경 (400 에러 해결)
        "size": 15,
        "sort": "distance"
    }
    
    try:
        res = requests.get(url, headers=headers, params=params)
        return Response(res.json())
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_route(request):
    """길찾기 경로 좌표 반환"""
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    url = "https://apis-navi.kakaomobility.com/v1/directions"
    headers = {
        "Authorization": f"KakaoAK {KAKAO_REST_KEY}",
        "Content-Type": "application/json"
    }
    params = { "origin": origin, "destination": destination, "priority": "RECOMMEND" }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        line_path = []
        if 'routes' in data:
            for route in data['routes']:
                for section in route['sections']:
                    for road in section['roads']:
                        for i in range(0, len(road['vertexes']), 2):
                            line_path.append({"lat": road['vertexes'][i+1], "lng": road['vertexes'][i]})
        return Response({"path": line_path})
    except Exception as e:
        return Response({"error": str(e)}, status=500)