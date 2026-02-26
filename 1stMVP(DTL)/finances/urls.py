'''
11/07 pjt06 url.py 생성
'''


from django.urls import path
from . import views
app_name = 'finances' 

urlpatterns = [
    path('recommend/', views.recommend_financial_products, name='recommend'),
    path("api/dividend-ranking/", views.dividend_ranking_api, name="dividend_ranking_api"), # 11/20 추가
]
