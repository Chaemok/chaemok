# backend/finlife/admin.py
from django.contrib import admin
from .models import DepositProduct, DepositOptions, SavingProduct, SavingOptions, ExchangeRate, AssetPrice

# 1. 예금 옵션을 상품 페이지에서 바로 보기 위한 Inline 설정
class DepositOptionsInline(admin.TabularInline):
    model = DepositOptions
    extra = 0 # 추가 빈 칸 표시 안 함

class DepositProductAdmin(admin.ModelAdmin):
    list_display = ('kor_co_nm', 'fin_prdt_nm', 'fin_prdt_cd') # 목록에서 보일 필드
    search_fields = ('kor_co_nm', 'fin_prdt_nm') # 검색 기능
    inlines = [DepositOptionsInline] # 상세 페이지에 금리 옵션 포함

# 2. 적금 옵션을 상품 페이지에서 바로 보기 위한 Inline 설정
class SavingOptionsInline(admin.TabularInline):
    model = SavingOptions
    extra = 0

class SavingProductAdmin(admin.ModelAdmin):
    list_display = ('kor_co_nm', 'fin_prdt_nm', 'fin_prdt_cd')
    search_fields = ('kor_co_nm', 'fin_prdt_nm')
    inlines = [SavingOptionsInline]

# 3. 환율 정보 관리
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('cur_nm', 'cur_unit', 'deal_bas_r', 'reference_date')
    list_filter = ('reference_date',) # 날짜별 필터링

# 4. 현물(금/은) 시세 관리
class AssetPriceAdmin(admin.ModelAdmin):
    list_display = ('asset_type', 'date', 'price')
    list_filter = ('asset_type', 'date')

# 모델 등록
admin.site.register(DepositProduct, DepositProductAdmin)
admin.site.register(SavingProduct, SavingProductAdmin)
admin.site.register(ExchangeRate, ExchangeRateAdmin)
admin.site.register(AssetPrice, AssetPriceAdmin)