# backend/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class User(AbstractUser):
    # [기본] username, password, email, first_name, last_name 포함
    
    # 1. 프로필 정보
    nickname = models.CharField(max_length=20, unique=True, null=True, blank=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    
    # 2. 금융 정보
    money = models.BigIntegerField(default=0, blank=True, null=True)
    salary = models.BigIntegerField(default=0, blank=True, null=True)
    
    # 3. 직업군
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

    # 4. [삭제됨] financial_products 
    # 이유: finlife 앱의 모델에서 related_name으로 역참조(subscribed_deposits 등)를 이미 제공함.
    # 여기서 또 정의하면 관계가 중복되어 혼란을 줌.
    
    # 5. 투자 성향
    RISK_CHOICES = [
        (1, '안정형'), (2, '안정추구형'), (3, '위험중립형'),
        (4, '적극투자형'), (5, '공격투자형'),
    ]
    risk_appetite = models.IntegerField(choices=RISK_CHOICES, default=3)

    # 6. 만나이 계산
    @property
    def age(self):
        if not self.birth_date:
            return 0
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def __str__(self):
        return self.username