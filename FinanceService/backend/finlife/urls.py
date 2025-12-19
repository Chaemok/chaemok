from django.urls import path
from . import views

urlpatterns = [
    # 금융 상품 조회 (Class-based)
    path('deposits/', views.DepositProductListAPIView.as_view(), name='deposit_list'),
    path('savings/', views.SavingProductListAPIView.as_view(), name='saving_list'),
    
    # 주식 데이터 (Class-based)
    path('stocks/top/', views.StockTopAPIView.as_view(), name='stock_top'),
    
    # 상품 가입 및 추천 (Function-based)
    path('deposits/join/<int:option_pk>/', views.join_deposit_option, name='join_deposit'),
    path('deposits/recommend/', views.recommend_products, name='recommend_products'),
    path('joined-products/', views.joined_products, name='joined_products'),
    path('stocks/recommend/', views.recommend_stocks, name='recommend_stocks'),
    
    # 외부 API 연동 (Function-based)
    path('exchange-rate/', views.exchange_rate, name='exchange_rate'),
    path('news/', views.finance_news_view, name='finance_news'),
    path('map-search/', views.map_search_proxy, name='map_search'),
    path('bank-products/', views.get_bank_products, name='bank_products'),
]