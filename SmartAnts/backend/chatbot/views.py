import requests
import json
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from finlife.models import DepositOptions, ExchangeRate

def get_smart_ants_context():
    """
    🐜 SmartAnts DB에서 실시간 금융 데이터를 요약해오는 함수
    """
    try:
        top_deposits = DepositOptions.objects.select_related('product').order_by('-intr_rate2')[:3]
        deposit_info = "\n".join([
            f"* {opt.product.kor_co_nm} {opt.product.fin_prdt_nm}: {opt.intr_rate2}%" 
            for opt in top_deposits
        ])

        rates = ExchangeRate.objects.filter(cur_unit__in=['USD', 'JPY(100)', 'EUR'])
        rate_info = "\n".join([f"* {r.cur_nm}({r.cur_unit}): {r.deal_bas_r}원" for r in rates])

        return f"[실시간 추천 예적금]\n{deposit_info}\n\n[실시간 환율 현황]\n{rate_info}"
    except Exception:
        return "현재 금융 데이터를 불러올 수 없어 일반 상식으로 답변해줘."

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_bot(request):
    user_message = request.data.get('message', '')
    history = request.data.get('history', []) 
    user = request.user
    
    gms_key = getattr(settings, 'GMS_KEY', None)
    endpoint_base = getattr(settings, 'GMS_ENDPOINT_BASE', None)
    
    if not gms_key or not endpoint_base:
        return Response({'answer': 'AntsBot 설정 오류가 발생했습니다. 🐜💦'}, status=500)

    # 유저 정보 요약
    try:
        joined_products = user.joined_deposits.all()
        joined_info = ", ".join([p.product.fin_prdt_nm for p in joined_products]) if joined_products else "아직 가입 상품이 없으시네요!"
    except Exception:
        joined_info = "정보 조회 중"

    market_context = get_smart_ants_context()

    # 🐜 AntsBot 페르소나 (답변 구조 강제 및 톤앤매너 최적화)
    system_instruction = f"""너는 'SmartAnts'의 유능한 금융 비서 'AntsBot'이야. 
유저({getattr(user, 'nickname', user.username)})에게 전문적이면서도 친절한 '스마트 브리핑'을 제공해.

[답변 구조 가이드라인 - 매우 중요]
1. (두괄식) 유저의 질문에 대한 답변을 한 줄로 요약해서 시작해.
2. (본론) 관련 데이터나 기능을 불렛포인트(*)로 간결하게 나열해.
3. (인사이트) 비서로서 유저에게 도움이 될 만한 짧은 조언이나 의견을 1~2문장 덧붙여.
4. (길이 제한) 전체 길이는 공백 포함 200~400자 사이로 유지해. (너무 짧거나 길지 않게)

[SmartAnts 주요 기능 지침]
- 실시간 금리 비교: 모든 은행 데이터를 분석해 최고 수익률 상품을 찾아줌.
- 환율 모니터링: 실시간 환율 정보를 제공해 환테크 타이밍을 잡아줌.
- 맞춤 추천: 유저의 가입상품({joined_info})과 시장 상황을 비교 분석함.

[실시간 참고 데이터]
{market_context}

[톤앤매너]
- 똑똑한 비서처럼 신뢰감 있는 말투를 써.
- 답변 끝에는 반드시 🐜 이모지를 하나 붙여줘."""

    # 대화 구성
    contents = []
    # 문맥 유지를 위해 최근 2~3쌍의 대화만 포함하여 집중력 높임
    for h in history[-4:]: 
        role = "model" if h['role'] == 'assistant' else "user"
        contents.append({"role": role, "parts": [{"text": h['content']}]})
    
    contents.append({
        "role": "user",
        "parts": [{"text": f"지침: {system_instruction}\n\n질문: {user_message}"}]
    })

    endpoint = f"{endpoint_base}?key={gms_key}"
    data = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.6,       # 👈 너무 딱딱하지 않게 0.6 설정
            "maxOutputTokens": 700,   
            "topP": 0.85,
        }
    }

    try:
        response = requests.post(endpoint, json=data, timeout=12)
        response.raise_for_status()
        result = response.json()
        
        bot_answer = result['candidates'][0]['content']['parts'][0]['text']
        return Response({'answer': bot_answer})

    except Exception as e:
        print(f"❌ AntsBot 에러: {e}")
        return Response({'answer': '개미굴 통신망에 장애가 생겼어요! 다시 물어봐줘 🐜💦'}, status=500)