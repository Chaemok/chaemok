# finances/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .ranking_service import get_dividend_ranking

@login_required
def recommend_financial_products(request):
    # 금융 상품 추천을 위한 로직을 작성합니다.
    return render(request, 'finances/recommend.html')

# 추가 11/20
def dividend_ranking_api(request):
    base_date, df = get_dividend_ranking()
    rows = df.to_dict(orient="records")

    return JsonResponse(
        {
            "base_date": base_date,
            "count": len(rows),
            "rows": rows,
        },
        json_dumps_params={"ensure_ascii": False}
    )