# ai_analysis/urls.py (파일을 새로 만드삼!)
from django.urls import path
from . import views

urlpatterns = [
    # 🐜 http://localhost:8000/api/ai/briefing/ 으로 접속하면 실행됨
    path('briefing/', views.get_ai_briefing, name='ai-briefing'),
]