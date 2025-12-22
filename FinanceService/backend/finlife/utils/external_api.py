# finlife/utils/external_api.py
import requests
from pykis import PyKis

# 🐜 발급받은 키들을 여기에 입력 (실전에서는 .env 파일 추천)
KIS_CONFIG = {
    'appkey': 'PSdmkbvFT2FS9TOsBB6QnkFyclrtMdyhmhKZ',
    'appsecret': 'jVmTq3aHR0TJk5rc0p+jDCqsKwCKscHsR5IJHmieo0nZV7+sc0wuUBoylIO4s0XNelLvhTBfyFLXHXAcdzmmV8REGE02a2qiS59XpMdkEl3kKqIuyDq8UBFFQkiQYlri1JTcpDYDJlzEDzTIoxYN841CZc3Ih/zQ4lx/g7Z8F+Fk2lvTImk=',
    'virtual': False  # 모의투자계좌일 때 True
}
GOLD_API_KEY = 'goldapi-980ssmjgvm0ob-io'

def get_kis_data(code, is_index=False):
    """
    🐜 만능 함수: 종목 코드만 주면 시세를 가져옴
    is_index: True면 지수(코스피 등), False면 일반 주식
    """
    try:
        kis = PyKis(**KIS_CONFIG)
        
        # 1. 타입에 따라 객체 생성
        target = kis.index(code) if is_index else kis.stock(code)
        price = target.price()
        
        # 2. 데이터 추출 (지수와 주식의 필드명이 미세하게 다를 수 있음)
        current_val = price.bstp_nmix_prpr if is_index else price.stck_prpr
        
        # 3. 공통 포맷팅 로직
        raw_val = str(current_val).replace(',', '')
        final_val = float(raw_val) if '.' in raw_val else int(raw_val)
        
        return {
            "code": code,
            "name": getattr(target, 'name', code),
            "value": f"{final_val:,.2f}" if is_index else f"{final_val:,}",
            "change": getattr(price, 'prdy_vrss', '0'),
            "rate": getattr(price, 'prdy_ctrt', '0'),
        }
    except Exception as e:
        print(f"KIS API ({code}) 에러: {e}")
        return None
        
def get_gold_silver_price():
    """GoldAPI.io로 금/은 시세 가져오기"""
    headers = {'x-access-token': GOLD_API_KEY, 'Content-Type': 'application/json'}
    
    # 금(XAU), 은(XAG) 요청 (달러 기준)
    try:
        gold_res = requests.get("https://www.goldapi.io/api/XAU/USD", headers=headers).json()
        silver_res = requests.get("https://www.goldapi.io/api/XAG/USD", headers=headers).json()
        
        return {
            "gold": gold_res.get('price'),   # 실시간 금 시세
            "silver": silver_res.get('price') # 실시간 은 시세
        }
    except Exception as e:
        print(f"GoldAPI 에러: {e}")
        return None