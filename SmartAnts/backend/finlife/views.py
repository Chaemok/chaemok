# backend/finlife/views.py
import re
import random
import requests
import pandas as pd
from datetime import datetime, timedelta

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

from django.conf import settings
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import DepositProduct, DepositOptions, SavingProduct, SavingOptions, ExchangeRate # DepositProduct, SavingProduct (s) 빠짐 나중에 추후에
from .serializers import (
    DepositProductSerializer, SavingProductSerializer, 
    ExchangeRateSerializer, JoinedDepositOptionSerializer, JoinedSavingOptionSerializer,
    DepositOptionsSerializer, SavingOptionsSerializer
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
NAVER_CLIENT_ID = settings.NAVER_CLIENT_ID
NAVER_CLIENT_SECRET = settings.NAVER_CLIENT_SECRET

User = get_user_model()
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

from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
from datetime import date

from .models import DepositOptions, SavingOptions
from .serializers import DepositOptionsSerializer, SavingOptionsSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_products(request):
    try:
        user = request.user
        
        # 🐜 1. 내가 이미 가입한 상품 ID 목록 추출 (중복 추천 방지용)
        # related_name이 'subscribed_deposits', 'subscribed_savings'로 설정되어 있어야 함
        my_deposit_ids = set(user.subscribed_deposits.values_list('id', flat=True))
        my_saving_ids = set(user.subscribed_savings.values_list('id', flat=True))
        my_joined_ids = my_deposit_ids | my_saving_ids # 합집합

        # ----------------------------------------
        # [알고리즘 1단계] 유사 유저 기반 필터링 (Collaborative Filtering)
        # ----------------------------------------
        all_users = User.objects.filter(birth_date__isnull=False, salary__isnull=False)
        
        # 데이터 부족 시 베스트 상품으로 이동
        if not all_users.exists():
            return get_best_products_response(user, my_joined_ids, is_no_data=True)

        df = pd.DataFrame(list(all_users.values('id', 'birth_date', 'salary', 'money')))
        
        # 내 정보가 없으면(신규) 베스트 상품
        if user.id not in df['id'].values:
            return get_best_products_response(user, my_joined_ids, is_new_user=True)

        # 나이 계산
        def calculate_age(born):
            today = date.today()
            return today.year - born.year if born else 30
        
        df['age'] = df['birth_date'].apply(calculate_age)
        df = df.drop(columns=['birth_date'])

        # 코사인 유사도 계산
        df = df.set_index('id')
        df.fillna(0, inplace=True) 
        similarity_matrix = cosine_similarity(df)
        
        user_idx = df.index.get_loc(user.id)
        
        # 유사 유저 상위 10명 (나 제외)
        similar_indices = similarity_matrix[user_idx].argsort()[::-1][1:11]
        similar_user_ids = df.index[similar_indices].tolist()
        
        # 유사 유저들의 가입 상품 수집
        similar_users = User.objects.filter(id__in=similar_user_ids)
        option_ids = []
        for u in similar_users:
            if hasattr(u, 'subscribed_deposits'):
                # 내가 가입 안 한 것만 추가
                for opt_id in u.subscribed_deposits.values_list('id', flat=True):
                    if opt_id not in my_joined_ids:
                        option_ids.append(opt_id)
            if hasattr(u, 'subscribed_savings'):
                for opt_id in u.subscribed_savings.values_list('id', flat=True):
                    if opt_id not in my_joined_ids:
                        option_ids.append(opt_id)

        # 추천할 게 없으면 베스트 상품
        if not option_ids:
            return get_best_products_response(user, my_joined_ids, is_no_data=True)
        
        # 가장 많이 가입된 상품 추출
        counter = Counter(option_ids)
        most_common_ids = [id for id, count in counter.most_common(10)] # 넉넉하게 10개 뽑음
        
        rec_deposits = list(DepositOptions.objects.filter(id__in=most_common_ids))
        rec_savings = list(SavingOptions.objects.filter(id__in=most_common_ids))
        
        candidates = rec_deposits + rec_savings

        # ----------------------------------------
        # [알고리즘 2단계] 투자 성향(Risk Appetite) 반영 정렬
        # ----------------------------------------
        # user.risk_appetite: 1(안정) ~ 5(공격)
        risk_score = user.risk_appetite if user.risk_appetite else 3
        
        if risk_score >= 4:
            # 공격형: 최고 우대 금리(intr_rate2) 높은 순
            candidates.sort(key=lambda x: x.intr_rate2 if x.intr_rate2 else 0, reverse=True)
            msg = f'{user.nickname}님의 공격적인 투자 성향에 맞춰 수익률이 높은 상품을 우선 추천해요! 🔥'
        
        elif risk_score <= 2:
            # 안정형: 기본 금리(intr_rate) 높은 순 (조건 없이 받는 돈 중요)
            candidates.sort(key=lambda x: x.intr_rate if x.intr_rate else 0, reverse=True)
            msg = f'{user.nickname}님의 신중한 성향을 고려해 기본 금리가 튼튼한 상품을 모았어요! 🛡️'
            
        else:
            # 중립형: 인기순(Counter 순서) 유지
            # candidates는 DB 쿼리 결과라 순서가 섞였을 수 있으니 counter 점수로 재정렬
            candidates.sort(key=lambda x: counter[x.id], reverse=True)
            msg = f'{user.nickname}님과 비슷한 자산/연령대 유저들이 가장 많이 선택한 상품이에요! 🐜'

        # 최종 상위 5~6개만 슬라이싱
        final_list = candidates[:6]

        combined_data = (
            DepositOptionsSerializer([x for x in final_list if isinstance(x, DepositOptions)], many=True).data + 
            SavingOptionsSerializer([x for x in final_list if isinstance(x, SavingOptions)], many=True).data
        )

        return Response({
            'type': 'custom',
            'message': msg,
            'data': combined_data
        })

    except Exception as e:
        print(f"!!! 추천 알고리즘 에러 !!!: {e}")
        # 에러 시에도 내가 가입한건 빼고 베스트 상품 추천
        my_deposit_ids = set(user.subscribed_deposits.values_list('id', flat=True))
        my_saving_ids = set(user.subscribed_savings.values_list('id', flat=True))
        return get_best_products_response(user, my_deposit_ids | my_saving_ids, is_no_data=True)


# 🐜 헬퍼 함수: 베스트 상품 추천 (중복 제외 기능 추가됨)
def get_best_products_response(user, joined_ids, is_new_user=False, is_no_data=False):
    # 내가 가입한 ID 제외하고 조회
    top_deposits = DepositOptions.objects.exclude(id__in=joined_ids).order_by('-intr_rate2')[:3]
    top_savings = SavingOptions.objects.exclude(id__in=joined_ids).order_by('-intr_rate2')[:3]
    
    combined_data = (
        DepositOptionsSerializer(top_deposits, many=True).data +
        SavingOptionsSerializer(top_savings, many=True).data
    )
    
    msg = '최고 금리 상품들을 모아봤어요!'
    if is_new_user:
        msg = '프로필 정보를 입력하시면 더 정확한 맞춤 추천이 가능해요! 인기 상품부터 둘러보세요.'
    elif is_no_data:
        msg = '비슷한 유저 데이터가 부족하여 금리순으로 보여드려요!'
        
    return Response({
        'type': 'best_rate',
        'message': msg,
        'data': combined_data
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def recommend_stocks(request):
    try:
        weights = {
            'w_div': float(request.GET.get('w_div', 0.3)), 
            'w_roe': float(request.GET.get('w_roe', 0.4)),
            'w_per': float(request.GET.get('w_per', 0.15)), 
            'w_pbr': float(request.GET.get('w_pbr', 0.15)),
        }
        # 🐜 [수정] limit=20 -> 200으로 변경!
        # 이제 프론트엔드로 200개를 보냅니다. 필터링은 프론트에서 합니다.
        return JsonResponse(get_stock_ranking(limit=200, weights=weights))
    except Exception as e: 
        return JsonResponse({'error': str(e)}, status=500)
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
    user_query = request.GET.get('query', '')
    category = request.GET.get('category', 'general')
    
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
    
    all_items = []
    
    try:
        # 1. 사용자 직접 검색 (최우선)
        if user_query:
            params = {"query": user_query, "display": 30, "sort": "date"}
            res = requests.get(url, headers=headers, params=params)
            if res.status_code == 200:
                all_items = res.json().get('items', [])

        # 2. '전체' 보기 (골고루 섞기)
        elif category == 'general':
            # 🐜 전체일 때는 이 키워드들을 조금씩 가져와서 섞습니다.
            keywords = ['경제', '증시', '반도체', '부동산', '금리']
            for kw in keywords:
                params = {"query": kw, "display": 10, "sort": "date"} # 키워드당 10개씩
                res = requests.get(url, headers=headers, params=params)
                if res.status_code == 200:
                    all_items.extend(res.json().get('items', []))
            random.shuffle(all_items)

        # 3. 특정 카테고리 선택 (확장됨!)
        else:
            # 🐜 [핵심] 카테고리별 꿀조합 검색어 맵
            keyword_map = {
                'stock': '주식 시장 코스피 실적',        # 증시
                'tech': 'IT 반도체 인공지능 AI 삼성전자', # IT/테크 (반도체 포함)
                'economy': '경제 정책 금리 물가 환율',    # 거시경제
                'crypto': '비트코인 가상화폐 블록체인',   # 코인
                'realestate': '부동산 아파트 분양 청약',  # 부동산
                'global': '미국 증시 연준 나스닥 엔비디아', # 해외주식
                'ipo': '공모주 청약 상장 IPO',           # 공모주 (인기!)
            }
            
            search_kw = keyword_map.get(category, '경제')
            
            # 특정 주제는 깊게 보기 위해 40개 요청
            params = {"query": search_kw, "display": 40, "sort": "date"}
            res = requests.get(url, headers=headers, params=params)
            if res.status_code == 200:
                all_items = res.json().get('items', [])

        # 4. 데이터 정제
        cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleaned_list = []
        
        for i in all_items:
            cleaned_list.append({
                "title": re.sub(cleaner, '', i['title']),
                "description": re.sub(cleaner, '', i['description']),
                "link": i['link'],
                "pubDate": i['pubDate']
            })
            
        return Response(cleaned_list[:100])
        
    except Exception as e:
        print(f"News Error: {e}")
        return Response({"error": "News failed"}, status=500)


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
    주식 상세 정보 (기간, 날짜 필터링 지원)
    """
    period = request.GET.get('period', '1d') # 기본값 1일
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    # 🐜 파라미터 전달
    data = get_stock_data(symbol, period=period, start_date=start, end_date=end) 
    
    if not data:
        return Response({"message": "데이터를 불러올 수 없습니다."}, status=404)
        
    return Response(data)