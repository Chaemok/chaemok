# ai_analysis/views.py 
import google.generativeai as genai
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from community.models import Post 
import json
import traceback

# 🐜 SSAFY GMS 전용 설정 (생략 없음)
genai.configure(
    api_key="S14P02DB09-afa432ce-5c10-4b60-8f6b-3273cace779a",
    client_options={
        "api_endpoint": "gms.ssafy.io/gmsapi"
    }
)

model = genai.GenerativeModel('gemini-2.0-flash') 

@api_view(['GET'])
def get_ai_briefing(request):
    # 1. 최근 24시간 게시글 수집
    yesterday = timezone.now() - timedelta(days=1)
    posts = Post.objects.filter(created_at__gte=yesterday).order_by('-created_at')[:30]
    
    if not posts:
        return Response({
            "title": "실시간 개미 브리핑",
            "summary": "최근 24시간 내에 올라온 소식이 아직 없네요. 🐜",
            "keywords": ["고요함"],
            "sentiment": "중립",
            "related_news": [],
            "analyzed_at": timezone.now().strftime("%Y.%m.%d %H:%M:%S")
        })

    post_text = "\n".join([f"[{p.category}] {p.title}: {p.content[:40]}" for p in posts])
    
    prompt = f"""
    당신은 금융 커뮤니티 분석가입니다. 다음 게시글들을 분석해서 투자자들에게 도움이 될 브리핑을 작성하세요.
    반드시 다음 JSON 구조를 지켜서 응답하세요:
    {{
        "title": "브리핑 제목",
        "summary": "전체 내용을 관통하는 한 문장 요약",
        "keywords": ["키워드1", "키워드2", "키워드3", "키워드4"],
        "sentiment": "긍정/부정/중립 중 하나",
        "news_topics": ["뉴스검색어1", "뉴스검색어2"]
    }}
    데이터: {post_text}
    """

    try:
        response = model.generate_content(
            prompt, 
            generation_config={"response_mime_type": "application/json"}
        )
        ai_data = json.loads(response.text)
        
        # 뉴스 데이터 생성
        topics = ai_data.get('news_topics', ['금융', '증시'])
        ai_data['related_news'] = [
            {
                "title": f"'{topics[0]}' 관련 시장 동향 리포트",
                "press": "🐜 개미경제",
                "url": "https://news.naver.com", 
                "time": "1시간 전"
            },
            {
                "title": f"전문가가 본 {topics[1]} 대응 전략",
                "press": "스마트인베스트",
                "url": "https://news.naver.com",
                "time": "3시간 전"
            }
        ]
        
        ai_data['analyzed_at'] = timezone.now().strftime("%Y.%m.%d %H:%M:%S")
        return Response(ai_data)
        
    except Exception as e:
        print(traceback.format_exc())
        return Response({
            "title": "분석 일시 중단",
            "summary": "AI 분석 중 오류가 발생했습니다.",
            "keywords": ["오류"],
            "sentiment": "알 수 없음",
            "related_news": [],
            "analyzed_at": timezone.now().strftime("%Y.%m.%d %H:%M:%S")
        }, status=500)