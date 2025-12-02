from django.shortcuts import render
from django.conf import settings  # ★ 이 줄이 꼭 필요합니다! (settings 불러오기)

def bank_map(request):
    # settings.py에 적은 키를 가져옵니다.
    kakao_key = settings.KAKAO_MAP_JS_KEY 

    context = {
        # HTML에서 {{ kakao_map_js_key }}라고 쓴 이름과 똑같이 맞춰줍니다.
        'kakao_map_js_key': kakao_key, 
    }

    return render(request, 'banks/bank_map.html', context)