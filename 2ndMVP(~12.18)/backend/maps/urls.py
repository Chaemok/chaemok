# backend/maps/urls.py (예시)

from django.urls import path
from . import views

urlpatterns = [
    # 🚨 Vue에서 호출하는 API 주소와 일치해야 합니다.
    # 만약 Vue에서 /api/finances/maps/search/ 로 호출한다면, 
    # settings.py의 root urlconf와 결합하여 주소가 매칭되어야 합니다.
    path('search/', views.map_search_places, name='map_search_places'),
]