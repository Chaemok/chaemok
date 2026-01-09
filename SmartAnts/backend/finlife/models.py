# backend/finlife/models.py
from django.db import models
from django.conf import settings


# --- [F03] 예금 상품 및 옵션 ---
# 1-1. 예금 상품 (기본 정보)
class DepositProduct(models.Model):
    # [F03-1] 중복 방지를 위한 고유 상품 코드 (unique=True 필수)
    fin_prdt_cd = models.CharField(max_length=100, unique=True)
    kor_co_nm = models.CharField(max_length=100)  # 은행명
    fin_prdt_nm = models.CharField(max_length=200) # 상품명
    etc_note = models.TextField(blank=True, null=True) # 금융 상품 설명
    join_deny = models.IntegerField(blank=True, null=True) # 가입 제한
    join_member = models.TextField(blank=True, null=True) # 가입 대상
    join_way = models.TextField(blank=True, null=True) # 가입 방법
    spcl_cnd = models.TextField(blank=True, null=True) # 우대 조건
    
    def __str__(self):
        return f"[{self.kor_co_nm}] {self.fin_prdt_nm}"

# 1-2. 예금 옵션 (가입 기간별 금리 정보) - [F03-3] 대응
class DepositOptions(models.Model):
    # 외래키를 통해 상품과 연결 (1:N 관계)
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.CharField(max_length=100)
    intr_rate_type_nm = models.CharField(max_length=100) # 저축 금리 유형명
    save_trm = models.IntegerField() # [F03-3] 저축 기간 (단위: 개월)
    intr_rate = models.FloatField(null=True) # 저축 금리
    intr_rate2 = models.FloatField(null=True) # 최고 우대 금리

    # [추가] 이 옵션(특정 기간 상품)에 가입한 유저들
    # 유저가 '상품'이 아닌 '특정 기간(예: 12개월)'에 가입하므로 여기에 두는 것이 더 정확해
    contract_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='subscribed_deposits', 
        blank=True
    )

# --- [F03 추가] 적금 상품 및 옵션 ---
# 2-1. 적금 상품 (기본 정보)
class SavingProduct(models.Model):
    fin_prdt_cd = models.CharField(max_length=100, unique=True)
    kor_co_nm = models.CharField(max_length=100)
    fin_prdt_nm = models.CharField(max_length=200)
    etc_note = models.TextField(blank=True, null=True)
    join_deny = models.IntegerField(blank=True, null=True)
    join_member = models.TextField(blank=True, null=True)
    join_way = models.TextField(blank=True, null=True)
    spcl_cnd = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"[{self.kor_co_nm}] {self.fin_prdt_nm}"
    
# 2-2. 적금 옵션 (기간별 금리)
class SavingOptions(models.Model):
    product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.CharField(max_length=100)
    intr_rate_type_nm = models.CharField(max_length=100)
    save_trm = models.IntegerField() # 저축 기간
    intr_rate = models.FloatField(null=True)
    intr_rate2 = models.FloatField(null=True)

    contract_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='subscribed_savings', 
        blank=True
    )


# --- [F03] 현물(금/은) 시세 데이터 ---
# 3.
class AssetPrice(models.Model):
    ASSET_CHOICES = [('gold', '금'), ('silver', '은')]
    asset_type = models.CharField(max_length=10, choices=ASSET_CHOICES)
    date = models.DateField()
    price = models.FloatField()

    class Meta:
        unique_together = ('asset_type', 'date') # 중복 방지

# --- [F06] 환율 정보 ---
# 4. 환율 정보 (기존 유지하되 중복 방지 고려)
class ExchangeRate(models.Model):
    cur_unit = models.CharField(max_length=50)      # 통화코드
    cur_nm = models.CharField(max_length=50)        # 국가/통화명
    ttb = models.CharField(max_length=50)           # 송금 받을 때
    tts = models.CharField(max_length=50)           # 송금 보낼 때
    deal_bas_r = models.CharField(max_length=50)    # 매매 기준율
    bkpr = models.CharField(max_length=50)          # 장부 가격
    reference_date = models.DateField(null=True, blank=True) # 기준 날짜
    created_at = models.DateTimeField(auto_now_add=True)

