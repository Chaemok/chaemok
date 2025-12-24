# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # 앱별 API 엔드포인트 (나중에 추가)
    path("api/accounts/", include("accounts.urls")),
    path("api/community/", include("community.urls")),
    path("api/finlife/", include("finlife.urls")),
    path('api/map/', include('map.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)