# backend/finances/models.py
from django.db import models
from django.contrib.auth import get_user_model # 👈 User 모델 참조를 위해 추가

User = get_user_model()
class DepositProduct(models.Model):
    bank_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    interest_rate = models.FloatField()
    highest_rate = models.FloatField(null=True, blank=True)
    join_term = models.CharField(max_length=50, blank=True)
    link_url = models.URLField(blank=True)
    rank_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    # 👇 [추가] 이 상품에 가입한 유저들 (Many-to-Many 관계)
    contract_user = models.ManyToManyField(
        User, 
        related_name='deposits', 
        blank=True
    )

    def __str__(self):
        return f"[{self.bank_name}] {self.product_name}"

class SavingProduct(models.Model):
    bank_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    interest_rate = models.FloatField()
    highest_rate = models.FloatField(null=True, blank=True)
    join_term = models.CharField(max_length=50, blank=True)
    link_url = models.URLField(blank=True)
    rank_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 가입 유저 (Many-to-Many)
    contract_user = models.ManyToManyField(
        User, 
        related_name='savings', 
        blank=True
    )

    def __str__(self):
        return f"[{self.bank_name}] {self.product_name}"

class ExchangeRate(models.Model):
    cur_unit = models.CharField(max_length=50)      # 통화코드 (USD, EUR 등)
    cur_nm = models.CharField(max_length=50)        # 국가/통화명 (미국 달러 등)
    ttb = models.CharField(max_length=50)           # 송금 받을 때
    tts = models.CharField(max_length=50)           # 송금 보낼 때
    deal_bas_r = models.CharField(max_length=50)    # 매매 기준율
    bkpr = models.CharField(max_length=50)          # 장부 가격
    reference_date = models.DateField(null=True, blank=True) #기준날짜
    created_at = models.DateTimeField(auto_now_add=True)