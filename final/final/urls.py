'''
11/07 pjt06 url.py 수정내용

path accounts 추가
path posts 추가
path finances 추가


'''
from django.contrib import admin
from django.urls import path, include
from .views import home   # ← 추가

urlpatterns = [
    path('', home, name='home'),  # ← 메인 페이지
    path('admin/', admin.site.urls),

     # 각 앱별 include
    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
    path('finances/', include('finances.urls')),
    path('notices/', include('notices.urls')),
    path("banks/", include("banks.urls")),

    # 공용(core) 기능 (테마 토글 등)
    path('core/', include('core.urls')), 
]


    
"""
URL configuration for pjt_06 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""