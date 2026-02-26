# backend/accounts/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# 우리가 정의한 User 모델 가져오기
User = get_user_model()

class CustomUserAdmin(UserAdmin):
    # 1. 유저 목록 화면에 보여질 컬럼들
    list_display = (
        'username', 
        'nickname', 
        'name', 
        'email', 
        'job', 
        'money', 
        'is_staff', 
    )

    # 2. 유저 목록 화면 오른쪽의 필터 옵션
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'job')

    # 3. 검색창에서 검색할 필드들 (아이디, 닉네임, 실명, 이메일로 검색 가능)
    search_fields = ('username', 'nickname', 'name', 'email')

    # 4. 유저 상세 수정 화면 구성 (섹션별로 나누기)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('개인 정보', {
            'fields': ('name', 'nickname', 'email', 'phone_number', 'birth_date', 'profile_image')
        }),
        ('금융 정보', {
            'fields': ('job', 'money', 'salary')
        }),
        ('권한', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('중요 날짜', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

# 커스텀한 Admin 클래스로 등록
admin.site.register(User, CustomUserAdmin)