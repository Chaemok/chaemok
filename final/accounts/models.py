'''
11/07 F02 models.py 수정

- CustomUser class 생성

'''
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # 추가 필드 예시
    nickname = models.CharField(
        max_length=50,
        unique=True,      # 값이 있으면 서로 달라야 함
        null=True,        # DB에 NULL 허용 → 여러 명이 닉네임 없이 있어도 OK
        blank=True,       # 폼에서 빈 값 허용 (createsuperuser 등)
    )  
    birthdate = models.DateField(null=True, blank=True)  # 생년월일 필드
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # 프로필 이미지 필드
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username