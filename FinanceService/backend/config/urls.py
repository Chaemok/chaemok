# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT 토큰 발급/갱신
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 앱별 API 엔드포인트 (나중에 추가)
    path("api/accounts/", include("accounts.urls")),
    path("api/community/", include("community.urls")),
    path("api/finlife/", include("finlife.urls")),
    path('api/ai/', include('ai_analysis.urls')),
    path('api/map/', include('map.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)