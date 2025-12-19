# backend/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class User(AbstractUser):
    # [기본] username, password, email, first_name, last_name 포함
    
    # 1. 프로필 정보
    nickname = models.CharField(max_length=20, unique=True, null=True, blank=True)
    name = models.CharField(max_length=30, blank=True, null=True) # 실명 (수정 불가용)
    phone_number = models.CharField(max_length=15, blank=True, null=True) # 핸드폰 번호 추가
    birth_date = models.DateField(blank=True, null=True) # 생년월일 (나이 계산용)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True) # 프로필 사진
    
    # 2. 금융 정보 (입력하기 싫으면 안 해도 됨 -> blank=True, null=True)
    money = models.BigIntegerField(default=0, blank=True, null=True)  # 자산
    salary = models.BigIntegerField(default=0, blank=True, null=True) # 연봉
    
    # 3. 직업군 (선택형)
    JOB_CHOICES = [
        ('student', '학생'),
        ('employee', '직장인'),
        ('civil_servant', '공무원'),
        ('professional', '전문직'),
        ('freelancer', '프리랜서'),
        ('business', '사업자'),
        ('housewife', '주부'),
        ('unemployed', '무직'),
        ('etc', '기타'),
    ]
    job = models.CharField(max_length=20, choices=JOB_CHOICES, blank=True, null=True)

    # 4. [추가] 가입한 금융 상품 목록 (명세서 F02 필수 요구사항)
    # 실제 예적금 모델(예: finlife.DepositProducts)과 ManyToMany 연결 필요
    # 아직 모델이 없다면 'finlife.DepositOptions' 등으로 연결할 예정임을 주석 처리
    financial_products = models.ManyToManyField('finlife.DepositOptions', blank=True, related_name='subscribed_users')
    # 5. [추가] 투자 성향 (AI 추천 F09 고도화용)
    RISK_CHOICES = [
        (1, '안정형'), (2, '안정추구형'), (3, '위험중립형'),
        (4, '적극투자형'), (5, '공격투자형'),
    ]
    risk_appetite = models.IntegerField(choices=RISK_CHOICES, default=3)

    # 6. 만나이 자동 계산 (DB에 저장 안 하고 필요할 때만 계산)
    @property
    def age(self):
        if not self.birth_date:
            return 0
        today = date.today()
        # 생일 지났으면 그대로, 안 지났으면 -1
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def __str__(self):
        return self.username