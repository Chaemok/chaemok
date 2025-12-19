# backend/finances/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.core.cache import cache
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .utils import get_stock_ranking
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import FinanceDataReader as fdr
import os

# 모델 및 시리얼라이저 임포트
# ⚠️ User는 여기서 직접 import 하지 않습니다.
from .models import DepositProduct, SavingProduct, ExchangeRate
from .serializers import DepositProductSerializer, SavingProductSerializer, ExchangeRateSerializer
from .utils import get_stock_ranking

import traceback

# API KEY 설정
FINLIFE_API_KEY = os.environ.get("FINLIFE_API_KEY", "3c4cbc25442ea93a9a4361c35eb0cf14")
# ==========================================
# [핵심] 내부용 데이터 수집 함수 (Deposit & Saving)
# ==========================================
def fetch_and_save_products():
    """
    DB에 데이터가 없을 때 금융감독원 API를 호출하여
    예금과 적금 데이터를 한 번에 저장하는 함수
    """
    top_fin_grp_nos = ['020000', '030300'] # 은행 + 저축은행
    
    # --- 1. 예금(Deposit) 데이터 저장 ---
    for topFinGrpNo in top_fin_grp_nos:
        url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={FINLIFE_API_KEY}&topFinGrpNo={topFinGrpNo}&pageNo=1'
        try:
            response = requests.get(url).json()
            if response.get('result', {}).get('err_cd') == '000':
                base_list = response['result']['baseList']
                option_list = response['result']['optionList']

                for base in base_list:
                    if DepositProduct.objects.filter(bank_name=base['kor_co_nm'], product_name=base['fin_prdt_nm']).exists():
                        continue
                    
                    this_options = [o for o in option_list if o['fin_prdt_cd'] == base['fin_prdt_cd']]
                    max_rate = max([o.get('intr_rate2') or 0.0 for o in this_options]) if this_options else 0.0
                    basic_rate = this_options[0].get('intr_rate') or 0.0 if this_options else 0.0
                    note = base.get('etc_note') or '기타'
                    DepositProduct.objects.create(
                        bank_name=base['kor_co_nm'],
                        product_name=base['fin_prdt_nm'],
                        join_term=note[:50],
                        interest_rate=basic_rate,
                        highest_rate=max_rate,
                        link_url=base.get('fin_co_hompage', '')
                    )
        except Exception as e:
            print(f"예금 저장 중 오류: {e}")
            continue

    # --- 2. 적금(Saving) 데이터 저장 ---
    for topFinGrpNo in top_fin_grp_nos:
        url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={FINLIFE_API_KEY}&topFinGrpNo={topFinGrpNo}&pageNo=1'
        try:
            response = requests.get(url).json()
            if response.get('result', {}).get('err_cd') == '000':
                base_list = response['result']['baseList']
                option_list = response['result']['optionList']

                for base in base_list:
                    if SavingProduct.objects.filter(bank_name=base['kor_co_nm'], product_name=base['fin_prdt_nm']).exists():
                        continue
                    
                    this_options = [o for o in option_list if o['fin_prdt_cd'] == base['fin_prdt_cd']]
                    max_rate = max([o.get('intr_rate2') or 0.0 for o in this_options]) if this_options else 0.0
                    basic_rate = this_options[0].get('intr_rate') or 0.0 if this_options else 0.0
                    
                    note = base.get('etc_note') or '기타'
                    
                    SavingProduct.objects.create(
                        bank_name=base['kor_co_nm'],
                        product_name=base['fin_prdt_nm'],
                        join_term=note[:50],
                        interest_rate=basic_rate,
                        highest_rate=max_rate,
                        link_url=base.get('fin_co_hompage', '')
                    )
        except Exception as e:
            print(f"적금 저장 중 오류: {e}")
            continue


# ==========================================
# 1. 예금 목록 조회 API (스마트 조회 적용)
# ==========================================
class DepositProductListAPIView(APIView):
    """
    GET /api/finances/deposits/
    데이터가 없으면 자동으로 받아오고 목록 반환
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            if not DepositProduct.objects.exists():
                fetch_and_save_products()
            
            products = DepositProduct.objects.all().order_by('-highest_rate')
            serializer = DepositProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            # 🚨 500 에러 대신 구체적인 에러 내용을 반환해서 확인
            return Response({"error": str(e)}, status=500)


# ==========================================
# 2. 적금 목록 조회 API (스마트 조회 적용)
# ==========================================
class SavingProductListAPIView(APIView):
    """
    GET /api/finances/savings/
    데이터가 없으면 자동으로 받아오고 목록 반환
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if not SavingProduct.objects.exists():
            fetch_and_save_products()

        products = SavingProduct.objects.all().order_by('-highest_rate')
        serializer = SavingProductSerializer(products, many=True)
        return Response(serializer.data)


# ==========================================
# [옵션] 강제 업데이트 API
# ==========================================
@api_view(['GET'])
def force_update_products(request):
    fetch_and_save_products()
    return JsonResponse({"message": "금융 상품 데이터 강제 업데이트 완료!"})


# ==========================================
# 3. 기타 조회 및 기능
# ==========================================

class TopDepositProductAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        limit = int(request.query_params.get('limit', 5))
        qs = DepositProduct.objects.all().order_by('-highest_rate')[:limit]
        serializer = DepositProductSerializer(qs, many=True)
        return Response(serializer.data)

class StockTopAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            limit = int(request.GET.get("limit", 20))
        except ValueError:
            limit = 20

        cache_key = f"stock_ranking_{limit}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        data = get_stock_ranking(limit=limit)
        cache.set(cache_key, data, 60 * 60) 
        return Response(data)

# [가입/해지]
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_deposit_product(request, product_pk):
    product = get_object_or_404(DepositProduct, pk=product_pk)
    user = request.user

    # DepositProduct 모델의 M:N 필드 related_name='deposits'라고 가정
    # (SavingProduct는 'savings'라고 가정)
    if product.contract_user.filter(pk=user.pk).exists():
        product.contract_user.remove(user)
        message = "가입 취소되었습니다."
        is_joined = False
    else:
        product.contract_user.add(user)
        message = "상품에 가입되었습니다!"
        is_joined = True

    return Response({
        "message": message,
        "is_joined": is_joined
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def joined_products(request):
    user = request.user
    # User 모델에 related_name='deposits'가 설정되어 있어야 함
    products = user.deposits.all() 
    serializer = DepositProductSerializer(products, many=True)
    return Response(serializer.data)


    # 1. DB에 오늘 날짜의 데이터가 있는지 확인 (필터링 로직 필요하면 모델에 created_at 같은 날짜 필드가 있어야 함)
    # 여기서는 간단하게 "데이터가 아예 없거나" or "강제 업데이트"가 필요할 때만 호출한다고 가정할 수도 있지만,
    # 수출입은행 API는 비영업일(주말/공휴일)에는 데이터를 안 줍니다.
    # 따라서 가장 안전한 방법: 일단 DB꺼 보여주되, 너무 오래됐으면 업데이트 시도 로직을 짜는 것입니다.
    
    # [수정 제안] 간단하게: DB 데이터를 우선 비우고 새로 받아오거나(초기화), 
    # 혹은 기존 로직을 유지하되 serializer.data 리턴 전에 API 호출을 시도할 수도 있습니다.
    
    # 여기서는 "기존 데이터 싹 지우고 새로 받기" 전략이 가장 깔끔합니다 (데이터 양이 적으므로).
    # 단, 수출입은행 API가 실패(주말 등)하면 기존 데이터를 보여주는 안전장치를 둡니다.

@api_view(['GET'])
@permission_classes([AllowAny])
def exchange_rate(request):
    EXIM_API_KEY = "VMyu0svCx0AhAHQms9zCgdFuWrfIUFiu"
    
    # 1. 오늘 날짜 데이터가 있는지 확인 (레코드가 있고, 오늘 날짜인지 체크하면 더 좋음)
    # 여기서는 간단하게 "데이터가 없으면 가져온다" 로직 유지
    if not ExchangeRate.objects.exists():
        
        for i in range(7):
            target_date = datetime.now() - timedelta(days=i)
            search_date = target_date.strftime('%Y%m%d') # API 요청용 (YYYYMMDD)
            save_date = target_date.strftime('%Y-%m-%d') # DB 저장용 (YYYY-MM-DD)

            url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={EXIM_API_KEY}&data=AP01&searchdate={search_date}'

            try:
                response = requests.get(url, timeout=5, verify=False).json()
                
                if response:
                    ExchangeRate.objects.all().delete()
                    for item in response:
                        ExchangeRate.objects.create(
                            cur_unit=item.get('cur_unit'),
                            cur_nm=item.get('cur_nm'),
                            ttb=item.get('ttb', '0').replace(',', ''),
                            tts=item.get('tts', '0').replace(',', ''),
                            deal_bas_r=item.get('deal_bas_r', '0').replace(',', ''),
                            bkpr=item.get('bkpr', '0').replace(',', ''),
                            reference_date=save_date # 👈 [핵심] 기준 날짜 저장
                        )
                    break 
            except Exception as e:
                print(f"API 호출 실패 ({search_date}): {e}")
                continue

        # 비상용 더미 데이터 (날짜는 오늘로 설정)
        if not ExchangeRate.objects.exists():
            today = datetime.now().strftime('%Y-%m-%d')
            dummy_data = [
                {"cur_unit": "USD", "cur_nm": "미국 달러", "deal_bas_r": "1350"},
                {"cur_unit": "EUR", "cur_nm": "유로", "deal_bas_r": "1450"},
                {"cur_unit": "JPY(100)", "cur_nm": "일본 옌", "deal_bas_r": "900"},
            ]
            for d in dummy_data:
                ExchangeRate.objects.create(
                    cur_unit=d['cur_unit'], cur_nm=d['cur_nm'], 
                    deal_bas_r=d['deal_bas_r'], ttb=d['deal_bas_r'], tts=d['deal_bas_r'], bkpr=d['deal_bas_r'],
                    reference_date=today
                )

    rates = ExchangeRate.objects.all()
    serializer = ExchangeRateSerializer(rates, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def exchange_rate_history(request):
    """
    네이버 금융 '일별 시세' 크롤링
    GET /api/finances/exchange-rate/history/?symbol=USD
    """
    symbol = request.GET.get('symbol', 'USD')
    
    # 네이버 통화 코드 매핑
    code_map = {
        'USD': 'FX_USDKRW',
        'JPY(100)': 'FX_JPYKRW',
        'EUR': 'FX_EURKRW',
        'CNY': 'FX_CNYKRW',
    }
    code = code_map.get(symbol, 'FX_USDKRW')
    
    # 네이버 일별 시세 페이지 (iframe 내부 URL)
    url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd={code}&page=1"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        history_data = []
        rows = soup.select('table.tbl_exchange tbody tr')
        
        for row in rows:
            # 날짜, 매매기준율, 전일대비 등 추출
            cols = row.select('td')
            if len(cols) < 4: continue # 빈 줄 제외
            
            date = cols[0].text.strip()
            price = cols[1].text.strip()
            diff = cols[2].text.strip().replace('\n', '').replace('\t', '')
            
            # 상승/하락 아이콘 확인
            img_tag = cols[2].select_one('img')
            status = "보합"
            if img_tag:
                img_src = img_tag.get('src', '')
                if 'ico_up' in img_src: status = "상승"
                elif 'ico_down' in img_src: status = "하락"
            
            history_data.append({
                'date': date,
                'price': price,
                'diff': diff,
                'status': status
            })
            
        return JsonResponse(history_data, safe=False)
        
    except Exception as e:
        print(f"Crawling Error: {e}")
        return JsonResponse([], safe=False)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def exchange_rate_chart_data(request):
    """
    기간별 환율 차트 데이터 반환 (Source: Naver Finance via FDR)
    GET /api/finances/exchange-rate/chart-data/?symbol=USD&period=1mo
    """
    symbol = request.GET.get('symbol', 'USD')
    period = request.GET.get('period', '1mo') # 1w, 1mo, 3mo, 1y, 3y
    
    # FDR 심볼 매핑 (네이버 금융 기준)
    symbol_map = {
        'USD': 'USD/KRW',
        'JPY(100)': 'JPY/KRW',
        'EUR': 'EUR/KRW',
        'CNY': 'CNY/KRW',
        'GBP': 'GBP/KRW',
        'AUD': 'AUD/KRW',
        'CAD': 'CAD/KRW',
        'HKD': 'HKD/KRW',
        'SGD': 'SGD/KRW',
        'NZD': 'NZD/KRW',
        'CHF': 'CHF/KRW',
    }
    
    fdr_symbol = symbol_map.get(symbol, 'USD/KRW')
    
    # 기간 계산
    end_date = datetime.now()
    if period == '1w':
        start_date = end_date - timedelta(weeks=1)
    elif period == '1mo':
        start_date = end_date - timedelta(days=30)
    elif period == '3mo':
        start_date = end_date - timedelta(days=90)
    elif period == '1y':
        start_date = end_date - timedelta(days=365)
    elif period == '3y':
        start_date = end_date - timedelta(days=365*3)
    else:
        start_date = end_date - timedelta(days=90)

    try:
        # 데이터 가져오기 (Close 종가 기준)
        df = fdr.DataReader(fdr_symbol, start_date, end_date)
        
        # 차트용 JSON 변환
        labels = df.index.strftime('%Y-%m-%d').tolist()
        data = df['Close'].tolist()
        
        return JsonResponse({
            'labels': labels,
            'data': data,
            'min': min(data) if data else 0,
            'max': max(data) if data else 0
        })
    except Exception as e:
        print(f"Chart Data Error: {e}")
        return JsonResponse({'labels': [], 'data': []})
    
# [추천] - get_user_model 적용 완료 ✅
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_products(request):
    User = get_user_model() # 👈 [수정] 현재 활성화된 User 모델 클래스를 가져옴
    user = request.user
    
    # User 모델에 salary 필드가 있다고 가정 (없으면 0 처리)
    user_salary = getattr(user, 'salary', 0) or 0
    
    # 비슷한 유저 필터링
    # 주의: salary나 birth_date 필드가 User 모델에 실제로 있어야 에러가 안 납니다.
    query = Q(salary__range=(user_salary - 10000000, user_salary + 10000000))
    
    # birth_date가 있다면 아래 주석 해제하여 조건 추가 가능
    # if hasattr(user, 'birth_date') and user.birth_date:
    #     query |= Q(birth_date__year__range=(user.birth_date.year - 5, user.birth_date.year + 5))

    similar_users = User.objects.filter(query).exclude(id=user.id)
    
    recommended_products = DepositProduct.objects.filter(
        contract_user__in=similar_users
    ).annotate(
        join_count=Count('contract_user')
    ).order_by('-join_count')[:5]
    
    # 추천 데이터가 없으면 전체 인기 상품 반환
    if not recommended_products.exists():
        recommended_products = DepositProduct.objects.annotate(
            join_count=Count('contract_user')
        ).order_by('-join_count')[:5]

    serializer = DepositProductSerializer(recommended_products, many=True)
    return Response(serializer.data)

# [네이버 환율 크롤링]
@api_view(['GET'])
@permission_classes([AllowAny])
def exchange_rate_view(request):
    url = "https://finance.naver.com/marketindex/"
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        rates = []
        items = soup.select("#exchangeList > li")
        
        for item in items:
            name = item.select_one("h3.h_lst").text.strip()
            value = item.select_one("span.value").text.replace(',', '')
            change = item.select_one("span.change").text.strip()
            status_text = item.select_one("span.blind").text
            is_up = "상승" in status_text

            if any(x in name for x in ['USD', 'JPY', 'EUR', 'CNY']):
                rates.append({
                    "name": name,
                    "value": float(value),
                    "change": float(change),
                    "is_up": is_up
                })
        
        return Response(rates)
        
    except Exception as e:
        print(f"Crawling Error: {e}")
        return Response({"error": "환율 정보를 가져오는데 실패했습니다."}, status=500)

# [뉴스]
@api_view(['GET'])
@permission_classes([AllowAny])
def finance_news_view(request):
    NAVER_CLIENT_ID = "HuqovM0XqQzKa7kMeYBb"
    NAVER_CLIENT_SECRET = "dnwCJRQx3i"
    
    query = "경제"
    url = "https://openapi.naver.com/v1/search/news.json"
    
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = { "query": query, "display": 5, "sort": "sim" }
    
    try:
        res = requests.get(url, headers=headers, params=params)
        if res.status_code == 200:
            items = res.json().get('items', [])
            cleaned_items = []
            
            def remove_html(text):
                cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
                return re.sub(cleaner, '', text)

            for item in items:
                cleaned_items.append({
                    "title": remove_html(item['title']),
                    "link": item['link'],
                    "description": remove_html(item['description']),
                    "pubDate": item['pubDate']
                })
            return Response(cleaned_items)
        else:
            return Response({"error": "Naver API Error"}, status=res.status_code)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

# @api_view(['GET'])
# @permission_classes([AllowAny]) # 로그인 없이도 접근 가능하게 설정 (원하시면 IsAuthenticated로 변경)
# def recommend_stocks(request):
#     """
#     AI 주식 추천 데이터 반환
#     GET /api/finances/stocks/recommend/
#     """
#     try:
#         # ✨ 여기서 utils.py 의 분석 로직이 실행됩니다!
#         result = get_stock_ranking(limit=20) 
        
#         # 결과 반환 ({ 'base_date': '...', 'rows': [...] })
#         return JsonResponse(result)
        
#     except Exception as e:
#         print(f"Stock Recommendation Error: {e}")
#         return JsonResponse({'error': str(e)}, status=500)

# @api_view(['GET'])
# @authentication_classes([]) # ✨ [핵심 해결책] 이 줄을 추가해야 합니다! (인증 검사 생략)
# @permission_classes([AllowAny])
# def recommend_stocks(request):
#     print("🚀 [API 요청] 주식 추천 요청 받음! (인증 무시)") 
#     try:
#         result = get_stock_ranking(limit=20)
#         return JsonResponse(result)
        
#     except Exception as e:
#         print(f"🔥 [에러] 주식 추천 로직 실패: {e}")
#         print(traceback.format_exc())
#         return JsonResponse({'error': str(e)}, status=500)

def safe_float_get(request, key, default):
    """요청에서 key 값을 가져와 float으로 안전하게 변환합니다."""
    value = request.GET.get(key)
    if value is not None and value != '':
        try:
            return float(value)
        except ValueError:
            # 변환 실패 시 기본값 사용
            pass
    return default

@api_view(['GET'])
@authentication_classes([]) 
@permission_classes([AllowAny])
def recommend_stocks(request):
    try:
        # 프론트엔드에서 보낸 가중치 파라미터 받기 (없거나 오류 시 기본값 사용)
        weights = {
            'w_div': safe_float_get(request, 'w_div', 0.30), 
            'w_roe': safe_float_get(request, 'w_roe', 0.40),
            'w_per': safe_float_get(request, 'w_per', 0.15),
            'w_pbr': safe_float_get(request, 'w_pbr', 0.15),
        }
        
        # utils 함수에 가중치 전달
        result = get_stock_ranking(limit=20, weights=weights)
        
        return JsonResponse(result)
        
    except Exception as e:
        print(f"🔥 [에러] 주식 추천 로직 실패: {e}")
        print(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)