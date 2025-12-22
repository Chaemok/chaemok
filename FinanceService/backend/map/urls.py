# map/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 🐜 은행/증권/ATM 검색 API (api/map/map-search/)
    path('map-search/', views.map_search, name='map-search'),
    # 🐜 경로 좌표 데이터 API (api/map/route/)
    path('route/', views.get_route, name='get-route'),
]