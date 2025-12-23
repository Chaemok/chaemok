# finlife/utils/external_api.py
import yfinance as yf

# 🐜 채목이랑 합의한 글로벌 10대 지표 티커 매핑
TICKER_MAP = {
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

def get_global_market_data():
    """yfinance를 사용하여 10대 글로벌 지표를 한 번에 가져오기"""
    results = {}
    
    for name, symbol in TICKER_MAP.items():
        try:
            # 🐜 최신 데이터를 가져오기 위해 5일치 데이터를 요청 (휴장일 대비)
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d")
            
            if not hist.empty:
                # 가장 최근 종가와 직전 종가 추출
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                
                change = current_price - prev_price
                rate = (change / prev_price) * 100
                
                # 지수와 통화/원자재에 따라 소수점 포맷팅 차별화
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