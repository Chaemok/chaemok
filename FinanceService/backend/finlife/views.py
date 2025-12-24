# backend/finlife/views.py
import re
import requests
from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import DepositProduct, DepositOptions, SavingProduct, SavingOptions, ExchangeRate
from .serializers import (
    DepositProductSerializer, SavingProductSerializer, 
    ExchangeRateSerializer, JoinedDepositOptionSerializer, JoinedSavingOptionSerializer
)

# 🐜 [수정] 모든 외부 유틸리티를 안정적인 동기 방식으로 호출합니다.
from .utils.external_api import (
    get_global_market_data, 
    get_exchange_history_data, 
    get_spot_history_data,
    get_stock_data 
)
from .utils.quant_analysis import get_stock_ranking
from .utils.youtube_api import search_youtube_videos

# API KEY 설정
FINLIFE_API_KEY = getattr(settings, 'FINLIFE_API_KEY', "3c4cbc25442ea93a9a4361c35eb0cf14")
EXIM_API_KEY = getattr(settings, 'EXIM_API_KEY', "VMyu0svCx0AhAHQms9zCgdFuWrfIUFiu")
NAVER_CLIENT_ID = getattr(settings, 'NAVER_CLIENT_ID', "HuqovM0XqQzKa7kMeYBb")
NAVER_CLIENT_SECRET = getattr(settings, 'NAVER_CLIENT_SECRET', "dnwCJRQx3i")

# ==========================================
# [데이터 수집 및 상품 조회]
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

class StockTopAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = get_stock_ranking(limit=5)
        return Response(result)

# ==========================================
# [사용자 가입 및 상품 추천]
# ==========================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_deposit_option(request, option_pk):
    option = get_object_or_404(DepositOptions, pk=option_pk)
    if option.contract_user.filter(pk=request.user.pk).exists():
        option.contract_user.remove(request.user)
        return Response({"is_joined": False, "message": "가입 취소되었습니다."})
    option.contract_user.add(request.user)
    return Response({"is_joined": True, "message": "상품 가입이 완료되었습니다!"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_saving_option(request, option_pk):
    option = get_object_or_404(SavingOptions, pk=option_pk)
    if option.contract_user.filter(pk=request.user.pk).exists():
        option.contract_user.remove(request.user)
        return Response({"is_joined": False, "message": "적금 가입이 취소되었습니다."})
    option.contract_user.add(request.user)
    return Response({"is_joined": True, "message": "적금 가입이 완료되었습니다!"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def joined_products(request):
    deposit_opts = DepositOptions.objects.filter(contract_user=request.user)
    saving_opts = SavingOptions.objects.filter(contract_user=request.user)
    return Response({
        "joined_deposits": JoinedDepositOptionSerializer(deposit_opts, many=True).data,
        "joined_savings": JoinedSavingOptionSerializer(saving_opts, many=True).data,
        "total_count": deposit_opts.count() + saving_opts.count()
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_products(request):
    user = request.user
    salary = getattr(user, 'salary', 0) or 0
    assets = getattr(user, 'money', 0) or 0
    risk = getattr(user, 'risk_appetite', 3) or 3
    is_deposit_focus = assets > (salary * 2)
    
    if is_deposit_focus:
        base_query = DepositOptions.objects.select_related('product')
        p_type = "예금"
    else:
        base_query = SavingOptions.objects.select_related('product')
        p_type = "적금"

    if risk <= 2:
        recommended = base_query.order_by('-intr_rate')[:5]
        message = f"안정적인 자산 관리를 선호하는 회원님을 위해 금리가 높은 {p_type} 상품을 선정했습니다."
    elif risk >= 4:
        recommended = base_query.order_by('-intr_rate2')[:5]
        message = f"수익률을 추구하는 회원님을 위해 우대 혜택이 큰 {p_type} 상품들을 모았습니다."
    else:
        recommended = base_query.filter(save_trm__gte=12).order_by('-intr_rate2')[:5]
        message = f"밸런스가 좋은 {p_type} 상품을 추천합니다."

    serializer = JoinedDepositOptionSerializer(recommended, many=True)
    return Response({"message": message, "data": serializer.data})

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
# [외부 데이터 및 지표 - 안정적인 동기 방식]
# ==========================================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_market_status(request):
    """글로벌 시장 지표 (안전한 동기 방식)"""
    try:
        data = get_global_market_data() 
        return Response(data)
    except Exception as e:
        print(f"Market Status Error: {e}")
        return Response({"error": "데이터 로드 실패"}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def stock_detail_api(request, symbol):
    """주식 종목 상세 검색 및 차트 데이터 (안전한 동기 방식)"""
    try:
        data = get_stock_data(symbol) 
        if not data:
            return Response({"message": "종목을 찾을 수 없습니다."}, status=404)
        return Response(data)
    except Exception as e:
        print(f"Stock API Error: {e}")
        return Response({"error": "종목 조회 중 오류 발생"}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def exchange_history(request):
    """환율 차트 히스토리 (동기 방식)"""
    code = request.GET.get('code', 'USD')
    period = request.GET.get('period', '1mo')
    start = request.GET.get('start')
    end = request.GET.get('end')
    data = get_exchange_history_data(code, period, start, end)
    return JsonResponse(data, safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def spot_price_history(request):
    """금/은 시세 조회 (동기 방식)"""
    symbol_type = request.GET.get('type', 'GOLD')
    start = request.GET.get('start')
    end = request.GET.get('end')
    data = get_spot_history_data(symbol_type, start, end)
    return JsonResponse(data, safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def exchange_rate(request):
    """실시간 환율 목록 (DB 기반)"""
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
    category = request.GET.get('category', 'general')
    keyword_map = {
        'general': '금융 경제', 'stock': '주식 시장 전망', 'crypto': '비트코인 가상화폐',
        'realestate': '부동산 시장 분양', 'global': '미국 증시 금리', 'tech': '핀테크 AI 금융'
    }
    query = keyword_map.get(category, '금융 경제')
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
    params = {"query": query, "display": 10, "sort": "sim"}
    
    try:
        res = requests.get(url, headers=headers, params=params)
        items = res.json().get('items', [])
        cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleaned_list = []
        for i in items:
            cleaned_list.append({
                "title": re.sub(cleaner, '', i['title']),
                "description": re.sub(cleaner, '', i['description']),
                "link": i['link'],
                "pubDate": i['pubDate'][:16]
            })
        return Response(cleaned_list)
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
def youtube_search(request):
    keyword = request.GET.get('keyword', '재테크')
    videos = search_youtube_videos(keyword)
    return JsonResponse(videos, safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def stock_detail_api(request, symbol):
    """
    🐜 symbol 자리에 '삼성전자'가 들어와도 처리 가능하도록 설계
    """
    # 쿼리 파라미터가 아닌 URL 경로에서 '삼성전자'를 읽어옵니다.
    data = get_stock_data(symbol) 
    
    if not data:
        return Response({"message": "종목을 찾을 수 없습니다. (정확한 티커나 종목번호를 입력해주세요)"}, status=404)
        
    return Response(data)