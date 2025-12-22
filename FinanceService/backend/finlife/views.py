import os
import re
import requests
import traceback
import FinanceDataReader as fdr
from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import DepositProduct, DepositOptions, SavingProduct, SavingOptions, ExchangeRate
from .serializers import (
    DepositProductSerializer, SavingProductSerializer, 
    ExchangeRateSerializer, JoinedDepositOptionSerializer
)
from .utils.external_api import get_kis_data, get_gold_silver_price
from .utils.quant_analysis import get_stock_ranking

# API KEY 설정
FINLIFE_API_KEY = getattr(settings, 'FINLIFE_API_KEY', "3c4cbc25442ea93a9a4361c35eb0cf14")
EXIM_API_KEY = getattr(settings, 'EXIM_API_KEY', "VMyu0svCx0AhAHQms9zCgdFuWrfIUFiu")
NAVER_CLIENT_ID = getattr(settings, 'NAVER_CLIENT_ID', "HuqovM0XqQzKa7kMeYBb")
NAVER_CLIENT_SECRET = getattr(settings, 'NAVER_CLIENT_SECRET', "dnwCJRQx3i")

# ==========================================
# [데이터 수집] 예적금 정보 저장
# ==========================================
def fetch_and_save_products():
    top_fin_grp_nos = ['020000', '030300']
    product_types = [
        ('depositProductsSearch.json', DepositProduct, DepositOptions),
        ('savingProductsSearch.json', SavingProduct, SavingOptions)
    ]
    for filename, ProductModel, OptionModel in product_types:
        for top_no in top_fin_grp_nos:
            url = f'http://finlife.fss.or.kr/finlifeapi/{filename}?auth={FINLIFE_API_KEY}&topFinGrpNo={top_no}&pageNo=1'
            try:
                res = requests.get(url).json()
                if res.get('result', {}).get('err_cd') == '000':
                    base_list = res['result']['baseList']
                    option_list = res['result']['optionList']
                    for base in base_list:
                        product, _ = ProductModel.objects.get_or_create(
                            fin_prdt_cd=base['fin_prdt_cd'],
                            defaults={
                                'kor_co_nm': base['kor_co_nm'], 'fin_prdt_nm': base['fin_prdt_nm'],
                                'etc_note': base.get('etc_note'), 'join_deny': base.get('join_deny'),
                                'join_member': base.get('join_member'), 'join_way': base.get('join_way'),
                                'spcl_cnd': base.get('spcl_cnd'),
                            }
                        )
                        this_options = [o for o in option_list if o['fin_prdt_cd'] == base['fin_prdt_cd']]
                        for opt in this_options:
                            OptionModel.objects.get_or_create(
                                product=product, fin_prdt_cd=opt['fin_prdt_cd'],
                                intr_rate_type_nm=opt['intr_rate_type_nm'], save_trm=opt['save_trm'],
                                defaults={'intr_rate': opt.get('intr_rate'), 'intr_rate2': opt.get('intr_rate2')}
                            )
            except Exception as e:
                print(f"Error saving {ProductModel.__name__}: {e}")

# ==========================================
# [API Views] 금융 상품 및 지표
# ==========================================
class DepositProductListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        if not DepositProduct.objects.exists(): fetch_and_save_products()
        products = DepositProduct.objects.all().order_by('kor_co_nm')
        return Response(DepositProductSerializer(products, many=True).data)

class SavingProductListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        if not SavingProduct.objects.exists(): fetch_and_save_products()
        products = SavingProduct.objects.all().order_by('kor_co_nm')
        return Response(SavingProductSerializer(products, many=True).data)

# 🐜 [에러 해결 포인트] StockTopAPIView 추가
class StockTopAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = get_stock_ranking(limit=5)
        return Response(result)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_deposit_option(request, option_pk):
    option = get_object_or_404(DepositOptions, pk=option_pk)
    if option.contract_user.filter(pk=request.user.pk).exists():
        option.contract_user.remove(request.user)
        return Response({"is_joined": False, "message": "가입 취소되었습니다."})
    option.contract_user.add(request.user)
    return Response({"is_joined": True, "message": "상품 가입이 완료되었습니다!"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def joined_products(request):
    deposit_opts = DepositOptions.objects.filter(contract_user=request.user)
    return Response({
        "joined_deposits": JoinedDepositOptionSerializer(deposit_opts, many=True).data,
        "total_count": deposit_opts.count()
    })

# ==========================================
# [알고리즘 & 추천]
# ==========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_products(request):
    user = request.user
    user_salary = getattr(user, 'salary', 0) or 0
    query = Q(salary__range=(user_salary - 10000000, user_salary + 10000000))
    similar_users = get_user_model().objects.filter(query).exclude(id=user.id)
    recommended = DepositOptions.objects.filter(contract_user__in=similar_users).annotate(cnt=Count('contract_user')).order_by('-cnt')[:5]
    if not recommended.exists():
        recommended = DepositOptions.objects.all().order_by('-intr_rate2')[:5]
    return Response({"data": JoinedDepositOptionSerializer(recommended, many=True).data})

@api_view(['GET'])
@permission_classes([AllowAny])
def recommend_stocks(request):
    try:
        weights = {
            'w_div': float(request.GET.get('w_div', 0.3)), 'w_roe': float(request.GET.get('w_roe', 0.4)),
            'w_per': float(request.GET.get('w_per', 0.15)), 'w_pbr': float(request.GET.get('w_pbr', 0.15)),
        }
        return JsonResponse(get_stock_ranking(limit=20, weights=weights))
    except Exception as e: return JsonResponse({'error': str(e)}, status=500)

# ==========================================
# [외부 데이터] 환율, 뉴스, 지도
# ==========================================
@api_view(['GET'])
@permission_classes([AllowAny])
def exchange_rate(request):
    if not ExchangeRate.objects.exists():
        for i in range(7):
            search_date = (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
            url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={EXIM_API_KEY}&data=AP01&searchdate={search_date}'
            try:
                res = requests.get(url, verify=False, timeout=5)
                data = res.json()
                if data:
                    ExchangeRate.objects.all().delete()
                    for item in data:
                        ExchangeRate.objects.create(
                            cur_unit=item.get('cur_unit'), cur_nm=item.get('cur_nm'),
                            deal_bas_r=item.get('deal_bas_r', '0').replace(',', ''),
                            reference_date=datetime.now().strftime('%Y-%m-%d')
                        )
                    break
            except: continue
    rates = ExchangeRate.objects.all()
    return Response(ExchangeRateSerializer(rates, many=True).data)

@api_view(['GET'])
@permission_classes([AllowAny])
def finance_news_view(request):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
    params = {"query": "금융 상품", "display": 5, "sort": "sim"}
    try:
        res = requests.get(url, headers=headers, params=params)
        items = res.json().get('items', [])
        cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleaned = [{"title": re.sub(cleaner, '', i['title']), "link": i['link'], "pubDate": i['pubDate']} for i in items]
        return Response(cleaned)
    except: return Response({"error": "News failed"}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_bank_products(request):
    bank_name = request.GET.get('bank_name', '')
    clean_name = bank_name.replace("KB", "").replace("NH", "").split()[0] 
    products = DepositProduct.objects.filter(kor_co_nm__contains=clean_name)[:3]
    return Response(DepositProductSerializer(products, many=True).data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_stock_detail(request):
    """
    🐜 검색용 API: /api/finlife/stock-detail/?code=005930
    """
    code = request.GET.get('code')
    is_index = request.GET.get('type') == 'index'
    
    if not code:
        return Response({"error": "종목 코드가 필요합니다."}, status=400)
        
    data = get_kis_data(code, is_index=is_index)
    return Response(data)