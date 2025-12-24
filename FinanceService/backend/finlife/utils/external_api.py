# backend/finlife/utils/external_api.py
import yfinance as yf
import pandas as pd

# 🐜 기존 글로벌 10대 지표 티커 매핑
MARKET_TICKER_MAP = {
    "NASDAQ": "^IXIC",
    "S&P 500": "^GSPC",
    "KOSPI": "^KS11",
    "KOSDAQ": "^KQ11",
    "USD/KRW": "USDKRW=X",
    "JPY/KRW": "JPYKRW=X",
    "EUR/KRW": "EURKRW=X",
    "GOLD": "GC=F",
    "WTI OIL": "CL=F",
    "NIKKEI 225": "^N225",
    "HANG SENG": "^HSI"
}

# 1. 글로벌 시장 지표 가져오기 (기존 함수)
def get_global_market_data():
    results = {}
    for name, symbol in MARKET_TICKER_MAP.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d")
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change = current_price - prev_price
                rate = (change / prev_price) * 100
                
                is_index = symbol.startswith('^')
                results[name] = {
                    "value": f"{current_price:,.2f}" if is_index else f"{current_price:,.2f}",
                    "change": f"{change:+.2f}",
                    "rate": f"{rate:+.2f}%",
                    "isUp": change > 0
                }
            else:
                results[name] = None
        except Exception as e:
            print(f"yfinance 에러 ({name}): {e}")
            results[name] = None
    return results

# 🐜 2. [수정] 환율 차트 데이터 (기간 선택 + 날짜 직접 지정 지원)
def get_exchange_history_data(code, period="1mo", start_date=None, end_date=None):
    """
    환율 데이터를 가져옵니다.
    :param period: '1mo', '1y' 등 (버튼 클릭 시)
    :param start_date: 'YYYY-MM-DD' (직접 지정 시)
    :param end_date: 'YYYY-MM-DD'
    """
    symbol_map = {
        'USD': 'KRW=X', 'EUR': 'EURKRW=X', 'JPY(100)': 'JPYKRW=X',
        'CNH': 'CNYKRW=X', 'HKD': 'HKDKRW=X', 'GBP': 'GBPKRW=X',
        'AUD': 'AUDKRW=X', 'CAD': 'CADKRW=X'
    }
    ticker_symbol = symbol_map.get(code, 'KRW=X')
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # 🐜 날짜 지정 여부에 따라 분기 처리
        if start_date and end_date:
            hist = ticker.history(start=start_date, end=end_date)
        else:
            hist = ticker.history(period=period)
        
        history_data = []
        for date, row in hist.iterrows():
            price = row['Close']
            if code == 'JPY(100)': price *= 100
            
            history_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'rate': round(float(price), 2)
            })
        return history_data

    except Exception as e:
        print(f"yfinance 환율 에러 ({code}): {e}")
        return []

def get_spot_history_data(symbol_type, start_date=None, end_date=None):
    """
    금/은 선물 시세 데이터를 가져와 원화(KRW) 및 달러(USD)로 반환합니다.
    :param symbol_type: 'GOLD' 또는 'SILVER'
    :param start_date: 'YYYY-MM-DD'
    :param end_date: 'YYYY-MM-DD'
    """
    # 1. 티커 매핑 (안정적인 선물 데이터 사용)
    spot_map = {
        'GOLD': 'GC=F',   # 금 선물
        'SILVER': 'SI=F'  # 은 선물
    }
    ticker_symbol = spot_map.get(symbol_type, 'GC=F')
    
    try:
        # 2. 데이터 가져오기 (자산 & 환율)
        spot_ticker = yf.Ticker(ticker_symbol)
        rate_ticker = yf.Ticker("KRW=X") # 원/달러 환율
        
        # 날짜 설정
        if start_date and end_date:
            spot_hist = spot_ticker.history(start=start_date, end=end_date)
            rate_hist = rate_ticker.history(start=start_date, end=end_date)
        else:
            # 기본값: 1개월
            spot_hist = spot_ticker.history(period="1mo")
            rate_hist = rate_ticker.history(period="1mo")

        # 3. 데이터 병합 (날짜 기준 교집합)
        # 시간대 정보(timezone) 제거 후 병합
        spot_hist.index = spot_hist.index.tz_localize(None)
        rate_hist.index = rate_hist.index.tz_localize(None)
        
        # 같은 날짜끼리 합치기 (suffixes: 이름 충돌 시 붙일 꼬리표)
        merged = pd.merge(
            spot_hist['Close'], 
            rate_hist['Close'], 
            left_index=True, 
            right_index=True, 
            suffixes=('_spot', '_rate')
        )
        
        # 4. 원화 가격 계산 및 리스트 변환
        # 계산: 선물가격($) * 환율(원)
        merged['Close_KRW'] = merged['Close_spot'] * merged['Close_rate']
        
        history_data = []
        for date, row in merged.iterrows():
            history_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'rate_krw': round(float(row['Close_KRW']), 0), # 원화는 정수 (소수점 버림)
                'rate_usd': round(float(row['Close_spot']), 2) # 달러는 소수점 2자리
            })
            
        return history_data

    except Exception as e:
        print(f"yfinance 현물 에러 ({symbol_type}): {e}")
        return []