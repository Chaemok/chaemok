'''
11/07 pjt06 urls.py 생성 F03
F07 login
F08 logout
F09 signup
F10 회원정보수정
F11 계정삭제
'''
from django.urls import path
from . import views

app_name = 'accounts' 

urlpatterns = [
    path('login/', views.login_view, name='login'), # F07 로그인 URL
    path('logout/', views.logout_view, name='logout'),  # F08 로그아웃 URL
    path('signup/', views.signup_view, name='signup'), # F09 회원가입 URL

    path('profile/', views.profile_view, name='profile'),  # 프로필 페이지 URL
    path('profile/update/', views.update_profile, name='update_profile'),  # F10 회원 정보 수정 URL 추가
    path('delete', views.delete_account, name='delete_account'),  # F11 계정 삭제 URL 추가
    
    path("password/change/", views.change_password, name="change_password"),
    path("password/change/done/", views.change_password_done, name="change_password_done"), # F12 비밀번호 변경 URL 추가
    
    path("admin-view/", views.AdminView.as_view(), name="admin_view"),
    # 추가적인 URL 패턴들
]
