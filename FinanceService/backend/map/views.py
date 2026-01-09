# map/views.py
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def map_search(request):
    query = request.GET.get('query', '은행')
    rect = request.GET.get('rect')

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": f"KakaoAK {settings.KAKAO_REST_KEY}"
    }

    params = {
        "query": query,
        "size": 15,
        "sort": "distance",
        "category_group_code": "BK9" if "은행" in query else ""
    }

    if rect:
        params["rect"] = rect
    else:
        params["y"] = request.GET.get('lat', '37.5215')
        params["x"] = request.GET.get('lng', '126.9243')
        params["radius"] = 5000

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5)
        return Response(res.json())
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def get_route(request):
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')

    url = "https://apis-navi.kakaomobility.com/v1/directions"
    headers = {
        "Authorization": f"KakaoAK {settings.KAKAO_REST_KEY}",
        "Content-Type": "application/json"
    }
    params = {
        "origin": origin,
        "destination": destination,
        "priority": "RECOMMEND"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()

        line_path = []
        if 'routes' in data:
            for route in data['routes']:
                for section in route['sections']:
                    for road in section['roads']:
                        for i in range(0, len(road['vertexes']), 2):
                            line_path.append({
                                "lat": road['vertexes'][i+1],
                                "lng": road['vertexes'][i]
                            })

        return Response({"path": line_path})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
