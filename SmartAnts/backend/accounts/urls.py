# backend/accounts/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    # 1. dj-rest-auth 기본 기능 (로그인, 로그아웃, 비밀번호 변경, 유저 정보 조회/수정)
    # /accounts/login/, /accounts/logout/, /accounts/user/, /accounts/password/change/ 등 활성화
    path('', include('dj_rest_auth.urls')),

    # 2. dj-rest-auth 회원가입 기능
    # /accounts/registration/ 경로로 가입 처리
    path('registration/', include('dj_rest_auth.registration.urls')),

    # 3. 커스텀 기능 (회원 탈퇴 및 중복 확인)
    path('delete/', views.delete_account, name='delete_account'),
    path('check-username/<str:username>/', views.check_username, name='check_username'),
    path('check-nickname/<str:nickname>/', views.check_nickname, name='check_nickname'),

    path('verify-password/', views.verify_password),
]