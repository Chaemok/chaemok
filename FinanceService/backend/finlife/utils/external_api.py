# backend/finlife/utils/external_api.py
import yfinance as yf
import pandas as pd
from datetime import datetime

# 🐜 글로벌 시장 지표 티커 매핑
MARKET_TICKER_MAP = {
    "NASDAQ": "^IXIC",
    "S&P 500": "^GSPC",
    "KOSPI": "^KS11",
    "KOSDAQ": "^KQ11",
    "USD/KRW": "USDKRW=X",
    "GOLD": "GC=F",
}

def get_global_market_data():
    """메인 페이지용 글로벌 시장 지표 조회"""
    results = {}
    for name, symbol in MARKET_TICKER_MAP.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            if not hist.empty and len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change = current_price - prev_price
                rate = (change / prev_price) * 100
                results[name] = {
                    "value": f"{current_price:,.2f}",
                    "change": f"{change:+.2f}",
                    "rate": f"{rate:+.2f}%",
                    "isUp": change > 0
                }
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            results[name] = None
    return results

def get_krx_mapping():
    """
    네이버 금융 등의 데이터를 활용해 한국 상장사 종목명/종목코드 매핑을 가져옵니다.
    매번 호출하면 느리므로 캐싱하여 사용합니다.
    """
    global _stock_name_to_id_cache
    if _stock_name_to_id_cache:
        return _stock_name_to_id_cache
    
    try:
        # 한국거래소(KRX) 종목 리스트를 가져오는 간단한 방식 (또는 사전에 정의된 리스트 사용)
        # 실제 운영시에는 별도의 JSON 파일이나 DB 테이블로 관리하는 것이 가장 좋습니다.
        # 예시로 가장 많이 찾는 상위 종목들을 우선 매핑합니다.
        top_stocks = {
            "삼성전자": "005930", "SK하이닉스": "000660", "LG에너지솔루션": "373220",
            "삼성바이오로직스": "207940", "현대차": "005380", "기아": "000270",
            "셀트리온": "068270", "KB금융": "105560", "네이버": "035420", "NAVER": "035420",
            "카카오": "035720", "삼성생명": "032830", "신한지주": "055550", "포스코": "005490",
            "POSCO홀딩스": "005490", "에코프로": "086520", "에코프로비엠": "247540"
        }
        _stock_name_to_id_cache = top_stocks
        return _stock_name_to_id_cache
    except:
        return {}

def get_stock_data(query):
    """
    종목명(삼성전자) -> 종목번호(005930) 변환 후 시세 조회
    """
    try:
        query = query.strip()
        mapping = get_krx_mapping()
        
        # 1. 종목명으로 들어온 경우 번호로 변환
        if query in mapping:
            ticker_symbol = f"{mapping[query]}.KS"
        elif query.isdigit():
            # 이미 번호(005930)로 들어온 경우
            ticker_symbol = f"{query}.KS"
        else:
            # 미국 주식(NVDA 등) 혹은 매핑에 없는 이름은 그대로 시도
            ticker_symbol = query.upper()

        ticker = yf.Ticker(ticker_symbol)
        
        # 2. 데이터 가져오기
        hist = ticker.history(period="7d", interval="1h")
        
        # 3. 코스피(.KS)에서 실패 시 코스닥(.KQ)으로 재시도
        if hist.empty and ".KS" in ticker_symbol:
            ticker_symbol = ticker_symbol.replace(".KS", ".KQ")
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period="7d", interval="1h")

        if hist.empty:
            return None

        # 데이터 가공
        prices = [round(float(val), 2) for val in hist['Close'].tolist()]
        labels = [d.strftime('%m/%d %H:%M') for d in hist.index]
        
        return {
            "symbol": ticker_symbol,
            "name": query, # 사용자가 검색한 이름 유지
            "labels": labels,
            "prices": prices,
            "current": prices[-1],
            "change": round(prices[-1] - prices[0], 2)
        }
    except Exception as e:
        print(f"Stock Detail Error ({query}): {e}")
        return None

def get_exchange_history_data(code, period="1mo", start_date=None, end_date=None):
    """환율 히스토리 조회"""
    symbol_map = {'USD': 'KRW=X', 'EUR': 'EURKRW=X', 'JPY': 'JPYKRW=X'}
    ticker_symbol = symbol_map.get(code, 'KRW=X')
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period=period) if not (start_date and end_date) else ticker.history(start=start_date, end=end_date)
        return [{'date': d.strftime('%Y-%m-%d'), 'rate': round(float(v), 2)} for d, v in hist['Close'].items()]
    except: return []

# backend/finlife/utils/external_api.py

def get_spot_history_data(symbol_type, start_date=None, end_date=None):
    """
    금/은 선물 시세 데이터를 가져와 원화(KRW) 및 달러(USD)로 반환합니다.
    """
    spot_map = {'GOLD': 'GC=F', 'SILVER': 'SI=F'}
    ticker_symbol = spot_map.get(symbol_type, 'GC=F')
    
    try:
        spot_ticker = yf.Ticker(ticker_symbol)
        rate_ticker = yf.Ticker("USDKRW=X") # 원/달러 환율 티커 확인
        
        # 🐜 데이터 수집
        if start_date and end_date:
            spot_hist = spot_ticker.history(start=start_date, end=end_date)
            rate_hist = rate_ticker.history(start=start_date, end=end_date)
        else:
            spot_hist = spot_ticker.history(period="1mo")
            rate_hist = rate_ticker.history(period="1mo")

        if spot_hist.empty:
            return []

        # 🐜 시계열 병합을 위해 인덱스 정리 (타임존 제거)
        spot_hist.index = spot_hist.index.tz_localize(None)
        rate_hist.index = rate_hist.index.tz_localize(None)
        
        # 데이터가 있는 날짜 기준으로 합치기
        merged = pd.merge(
            spot_hist[['Close']], 
            rate_hist[['Close']], 
            left_index=True, 
            right_index=True, 
            how='inner', # 양쪽 다 데이터가 있는 날만
            suffixes=('_spot', '_rate')
        )
        
        # 데이터가 부족하면 환율 데이터를 앞뒤로 채움(fillna)
        if merged.empty:
            # 병합 실패 시 단순 spot 데이터만이라도 반환 시도
            return [{'date': d.strftime('%Y-%m-%d'), 'rate_usd': round(float(v), 2)} for d, v in spot_hist['Close'].items()]

        history_data = []
        for date, row in merged.iterrows():
            # 금 선물은 트로이온스(oz) 단위이므로 원화 계산 시 환율 적용
            usd_price = float(row['Close_spot'])
            krw_price = usd_price * float(row['Close_rate'])
            
            history_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'rate_krw': round(krw_price, 0), # 원화 정수
                'rate_usd': round(usd_price, 2)  # 달러 소수점 2자리
            })
            
        return history_data

    except Exception as e:
        print(f"yfinance Spot Error ({symbol_type}): {e}")
        return []