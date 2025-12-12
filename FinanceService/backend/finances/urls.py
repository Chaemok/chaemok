# backend/finances/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 1. 예금/적금 조회 (스마트 조회: 접속 시 데이터 없으면 자동 저장됨)
    path('deposits/', views.DepositProductListAPIView.as_view(), name='deposit_list'),
    path('savings/', views.SavingProductListAPIView.as_view(), name='saving_list'),
    
    # [수정됨] 기존의 개별 save URL들은 삭제하고, 강제 업데이트 URL 하나로 통합
    path('products/update/', views.force_update_products, name='force_update_products'),

    # 2. 예금 상세/추천 기능
    path('deposits/top/', views.TopDepositProductAPIView.as_view(), name='deposit_top'),
    path('deposits/recommend/', views.recommend_products, name='recommend_products'),
    path('deposits/<int:product_pk>/join/', views.join_deposit_product, name='join_deposit'),
    
    # 3. 마이페이지 관련
    path('joined-products/', views.joined_products, name='joined_products'),

    # 4. 주식/환율/뉴스
    path('stocks/top/', views.StockTopAPIView.as_view(), name='stock_top'),
    path('exchange-rate/', views.exchange_rate, name='exchange_rate'), # 수출입은행
    path('exchange-rate/live/', views.exchange_rate_view, name='exchange_rate_crawling'), # 네이버 크롤링
    path('exchange-rate/history/', views.exchange_rate_history, name='exchange_rate_history'),
    path('exchange-rate/chart-data/', views.exchange_rate_chart_data, name='chart_data'),
    path('news/', views.finance_news_view, name='finance_news'),

    # 5. 주식 추천 서비스
    path('stocks/recommend/', views.recommend_stocks, name='stock_recommendation'),
    
]