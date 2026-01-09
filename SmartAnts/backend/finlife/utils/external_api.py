# backend/finlife/utils/external_api.py
# backend/finlife/utils/external_api.py
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pykrx import stock

# 1. 환율 매핑 (기존 유지)
EXCHANGE_TICKER_MAP = {
    'USD': 'KRW=X', 'EUR': 'EURKRW=X', 'JPY(100)': 'JPYKRW=X',
    'CNH': 'CNYKRW=X', 'GBP': 'GBPKRW=X', 'HKD': 'HKDKRW=X',
    'SGD': 'SGDKRW=X', 'CAD': 'CADKRW=X', 'CHF': 'CHFKRW=X',
    'AUD': 'AUDKRW=X', 'NZD': 'NZDKRW=X',
}

# 2. 글로벌 지수 매핑
MARKET_TICKER_MAP = {
    "NASDAQ": "^IXIC", "S&P 500": "^GSPC", "KOSPI": "^KS11",
    "KOSDAQ": "^KQ11", "USD/KRW": "USDKRW=X", "GOLD": "GC=F",
    "HSI": "^HSI", # 홍콩 항셍
    "Nikkei 225": "^N225", # 일본 닛케이
    "Euro Stoxx 50": "^STOXX50E" # 유로 스톡스
}

# 3. 미국 인기 주식 매핑 (기존 유지)
US_STOCK_MAP = {
    "애플": "AAPL", "마이크로소프트": "MSFT", "엔비디아": "NVDA",
    "구글": "GOOGL", "아마존": "AMZN", "메타": "META", "테슬라": "TSLA",
    "TSMC": "TSM", "AMD": "AMD", "인텔": "INTC", "마이크론": "MU",
    "브로드컴": "AVGO", "퀄컴": "QCOM", "ARM": "ARM", "슈퍼마이크로": "SMCI",
    "스타벅스": "SBUX", "코카콜라": "KO", "맥도날드": "MCD", "나이키": "NKE",
    "넷플릭스": "NFLX", "디즈니": "DIS", "코스트코": "COST", "월마트": "WMT",
    "화이자": "PFE", "모더나": "MRNA", "보잉": "BA", "에어비앤비": "ABNB",
    "쿠팡": "CPNG", "로블록스": "RBLX", "팔란티어": "PLTR", "코인베이스": "COIN",
    "QQQ": "QQQ", "나스닥": "QQQ", "SPY": "SPY", "S&P500": "SPY", "VOO": "VOO",
    "SOXX": "SOXX", "반도체": "SOXX", "TQQQ": "TQQQ", "SOXL": "SOXL", "속슬": "SOXL",
    "티큐": "TQQQ", "SQQQ": "SQQQ", "SOXS": "SOXS", "엔비디아2배": "NVDL", "테슬라2배": "TSLL"
}

_KRX_TICKER_CACHE = {}

# ... (get_latest_business_day, get_krx_mapping 기존 코드 유지 - 생략) ...
def get_latest_business_day():
    date = datetime.now()
    while date.weekday() > 4 or (date.weekday() == 0 and date.hour < 9): date -= timedelta(days=1)
    return date.strftime("%Y%m%d")

def get_krx_mapping():
    global _KRX_TICKER_CACHE
    if _KRX_TICKER_CACHE: return _KRX_TICKER_CACHE
    try:
        target_date = get_latest_business_day()
        for ticker in stock.get_market_ticker_list(target_date, market="KOSPI"):
            _KRX_TICKER_CACHE[stock.get_market_ticker_name(ticker)] = f"{ticker}.KS"
        for ticker in stock.get_market_ticker_list(target_date, market="KOSDAQ"):
            _KRX_TICKER_CACHE[stock.get_market_ticker_name(ticker)] = f"{ticker}.KQ"
        for ticker in stock.get_etf_ticker_list(target_date):
            _KRX_TICKER_CACHE[stock.get_etf_ticker_name(ticker)] = f"{ticker}.KS"
        return _KRX_TICKER_CACHE
    except: return {}

def get_global_market_data():
    results = {}
    for name, symbol in MARKET_TICKER_MAP.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            if not hist.empty and len(hist) >= 2:
                curr, prev = hist['Close'].iloc[-1], hist['Close'].iloc[-2]
                change = curr - prev
                rate = (change / prev) * 100
                results[name] = {
                    "value": f"{curr:,.2f}",
                    "change": f"{change:+.2f}",
                    "rate": f"{rate:+.2f}%",
                    "isUp": change > 0,
                    "symbol": symbol # 🐜 모달에서 차트 그릴 때 필요해서 추가
                }
        except: results[name] = None
    return results

# =========================================================
# 🐜 [대개조] 기간/날짜별 상세 주식 데이터 조회
# =========================================================
def get_stock_data(query, period="1d", start_date=None, end_date=None):
    query = query.strip()
    ticker_symbol = None
    
    # 1. 심볼 매핑 로직 (기존과 동일)
    krx_map = get_krx_mapping()
    if query in krx_map: ticker_symbol = krx_map[query]
    elif query in US_STOCK_MAP: ticker_symbol = US_STOCK_MAP[query]
    elif query in MARKET_TICKER_MAP.values(): ticker_symbol = query # 지수 심볼 직접 호출 시
    elif not query.replace('.','').isdigit() and not query.encode().isalpha():
        candidates = [name for name in krx_map.keys() if query in name]
        if candidates: ticker_symbol = krx_map[sorted(candidates, key=len)[0]]
    if not ticker_symbol:
        if query.isdigit(): ticker_symbol = f"{query}.KS"
        else: ticker_symbol = query.upper()

    try:
        # 2. 데이터 간격(Interval) 결정 로직 🐜
        interval = "1d"
        if start_date and end_date:
            # 커스텀 기간이면 기본 1일
            pass 
        else:
            # 프리셋 기간별 최적 간격
            if period == "1d": interval = "5m"   # 하루는 5분봉
            elif period == "5d": interval = "1h" # 일주일은 1시간봉
            elif period in ["1mo", "3mo"]: interval = "1d"
            elif period in ["6mo", "1y", "ytd", "max"]: interval = "1d"

        # 3. yfinance 호출
        ticker = yf.Ticker(ticker_symbol)
        
        if start_date and end_date:
            hist = ticker.history(start=start_date, end=end_date, interval="1d")
        else:
            hist = ticker.history(period=period, interval=interval)
        
        # 코스닥 재시도 로직
        if hist.empty and ticker_symbol.endswith('.KS') and query.isdigit():
            alt = ticker_symbol.replace('.KS', '.KQ')
            ticker = yf.Ticker(alt)
            if start_date and end_date:
                hist = ticker.history(start=start_date, end=end_date, interval="1d")
            else:
                hist = ticker.history(period=period, interval=interval)
            if not hist.empty: ticker_symbol = alt

        if hist.empty: return None

        # 4. 데이터 가공 (표 & 차트용 리스트)
        history_list = []
        for dt, row in hist.iterrows():
            close_val = row['Close']
            # 한국 시장은 소수점 제거, 미국은 2자리
            is_kr = ticker_symbol.endswith(('.KS', '.KQ'))
            
            history_list.append({
                "date": dt.strftime('%Y-%m-%d') if interval == '1d' else dt.strftime('%m/%d %H:%M'),
                "close": round(close_val, 0 if is_kr else 2),
                "open": round(row['Open'], 0 if is_kr else 2),
                "high": round(row['High'], 0 if is_kr else 2),
                "low": round(row['Low'], 0 if is_kr else 2),
                "volume": int(row['Volume'])
            })

        # 현재가 정보 (마지막 데이터)
        current_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[0] # 기간 내 시초가 기준 변동
        # *참고: 실제 전일 대비 등락은 info를 불러와야 정확하지만, 여기선 '조회 기간 내 변동'을 보여줌
        
        return {
            "symbol": ticker_symbol,
            "name": query, 
            "current": current_price,
            "change": current_price - prev_close,
            "currency": "KRW" if ticker_symbol.endswith(('.KS', '.KQ')) else "USD",
            "history": history_list # 🐜 차트와 표를 그릴 핵심 데이터
        }

    except Exception as e:
        print(f"Stock Error: {e}")
        return None

# ... (exchange, spot 함수 유지) ...
def get_exchange_history_data(code, period="1mo", start_date=None, end_date=None):
    # 기존 코드 그대로 유지
    ticker_symbol = EXCHANGE_TICKER_MAP.get(code)
    try:
        if ticker_symbol:
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period=period) if not (start_date and end_date) else ticker.history(start=start_date, end=end_date)
            if not hist.empty:
                return [{'date': d.strftime('%Y-%m-%d'), 'rate': round(float(r)*100 if '(100)' in code else float(r), 2)} for d, r in hist['Close'].items()]

        usd_krw = yf.Ticker("KRW=X").history(period=period)
        clean_code = code.split('(')[0]
        usd_target = yf.Ticker(f"{clean_code}=X").history(period=period)
        
        if usd_krw.empty or usd_target.empty: return []
        
        usd_krw.index = usd_krw.index.tz_localize(None)
        usd_target.index = usd_target.index.tz_localize(None)
        
        merged = pd.merge(usd_krw[['Close']], usd_target[['Close']], left_index=True, right_index=True, suffixes=('_krw', '_target'))
        
        data = []
        for d, r in merged.iterrows():
            rate = r['Close_krw'] / r['Close_target']
            if '(100)' in code: rate *= 100
            data.append({'date': d.strftime('%Y-%m-%d'), 'rate': round(rate, 2)})
        return data
    except: return []

def get_spot_history_data(symbol_type, start_date=None, end_date=None):
    # 기존 코드 그대로 유지
    map_code = {'GOLD': 'GC=F', 'SILVER': 'SI=F'}
    try:
        spot = yf.Ticker(map_code.get(symbol_type, 'GC=F'))
        rate = yf.Ticker("USDKRW=X")
        s_hist = spot.history(period="1mo")
        r_hist = rate.history(period="1mo")
        if s_hist.empty: return []
        s_hist.index = s_hist.index.tz_localize(None)
        r_hist.index = r_hist.index.tz_localize(None)
        merged = pd.merge(s_hist[['Close']], r_hist[['Close']], left_index=True, right_index=True, suffixes=('_s', '_r'))
        return [{'date': d.strftime('%Y-%m-%d'), 'rate_usd': round(row['Close_s'], 2), 'rate_krw': round(row['Close_s'] * row['Close_r'], 0)} for d, row in merged.iterrows()]
    except: return []


# import yfinance as yf
# import pandas as pd
# from datetime import datetime

# # 🐜 1. 환율 티커 매핑
# EXCHANGE_TICKER_MAP = {
#     'USD': 'KRW=X', 'EUR': 'EURKRW=X', 'JPY(100)': 'JPYKRW=X',
#     'CNH': 'CNYKRW=X', 'GBP': 'GBPKRW=X', 'HKD': 'HKDKRW=X',
#     'SGD': 'SGDKRW=X', 'CAD': 'CADKRW=X', 'CHF': 'CHFKRW=X',
#     'AUD': 'AUDKRW=X', 'NZD': 'NZDKRW=X',
# }

# # 🐜 2. 글로벌 지수 매핑
# MARKET_TICKER_MAP = {
#     "NASDAQ": "^IXIC", "S&P 500": "^GSPC", "KOSPI": "^KS11",
#     "KOSDAQ": "^KQ11", "USD/KRW": "USDKRW=X", "GOLD": "GC=F",
# }

# # 🐜 3. [NEW] 한국 주요 종목 이름 -> 티커 매핑 (인기 종목 하드코딩)
# # 실제 서비스에선 DB나 pykrx로 관리하지만, 데모용으론 이게 훨씬 빠르고 안정적입니다.
# KOREAN_STOCK_MAP = {
#     "삼성전자": "005930.KS", "SK하이닉스": "000660.KS", "LG에너지솔루션": "373220.KS",
#     "삼성바이오로직스": "207940.KS", "현대차": "005380.KS", "기아": "000270.KS",
#     "셀트리온": "068270.KS", "KB금융": "105560.KS", "네이버": "035420.KS", "NAVER": "035420.KS",
#     "카카오": "035720.KS", "삼성생명": "032830.KS", "신한지주": "055550.KS", "POSCO홀딩스": "005490.KS",
#     "에코프로": "086520.KQ", "에코프로비엠": "247540.KQ"
# }

# def get_global_market_data():
#     """글로벌 시장 지표 조회"""
#     results = {}
#     for name, symbol in MARKET_TICKER_MAP.items():
#         try:
#             ticker = yf.Ticker(symbol)
#             hist = ticker.history(period="2d")
#             if not hist.empty and len(hist) >= 2:
#                 curr = hist['Close'].iloc[-1]
#                 prev = hist['Close'].iloc[-2]
#                 change = curr - prev
#                 rate = (change / prev) * 100
#                 results[name] = {
#                     "value": f"{curr:,.2f}",
#                     "change": f"{change:+.2f}",
#                     "rate": f"{rate:+.2f}%",
#                     "isUp": change > 0
#                 }
#         except: results[name] = None
#     return results

# # =========================================================
# # 🐜 [핵심 구현] 주식 데이터 가져오기 (pass 제거됨!)
# # =========================================================
# def get_stock_data(query):
#     """
#     종목명('삼성전자') 또는 티커('AAPL', '005930.KS')를 받아 
#     현재가, 변동폭, 차트 데이터를 반환합니다.
#     """
#     query = query.strip()
    
#     # 1. 한국 종목명 매핑 확인 (예: '삼성전자' -> '005930.KS')
#     # 대소문자 무시하고 검색하기 위해 둘 다 upper 처리 등은 생략하고 단순 매칭
#     if query in KOREAN_STOCK_MAP:
#         ticker_symbol = KOREAN_STOCK_MAP[query]
#     elif query.isdigit(): 
#         # 숫자만 입력된 경우 (예: 005930) -> 코스피(.KS)로 가정
#         ticker_symbol = f"{query}.KS"
#     else:
#         # 그 외(영어 티커 등)는 그대로 사용 (예: TSLA, AAPL)
#         ticker_symbol = query.upper()

#     try:
#         # 2. yfinance 데이터 조회
#         ticker = yf.Ticker(ticker_symbol)
        
#         # 최근 7일치 1시간 간격 데이터 (차트용)
#         hist = ticker.history(period="7d", interval="1h")
        
#         # 2-1. 데이터가 없으면 코스닥(.KQ)으로 한 번 더 시도 (한국 주식인 경우)
#         if hist.empty and ticker_symbol.endswith('.KS'):
#             ticker_symbol = ticker_symbol.replace('.KS', '.KQ')
#             ticker = yf.Ticker(ticker_symbol)
#             hist = ticker.history(period="7d", interval="1h")

#         if hist.empty:
#             return None

#         # 3. 데이터 가공
#         # 마지막 종가 (현재가)
#         current_price = hist['Close'].iloc[-1]
#         # 시작가 (7일 전) - 변동 계산용
#         start_price = hist['Close'].iloc[0]
#         change = current_price - start_price
        
#         # 차트용 데이터 배열
#         # NaN 값 제거 및 소수점 처리
#         prices = [round(float(x), 0) if ticker_symbol.endswith(('KS', 'KQ')) else round(float(x), 2) for x in hist['Close'].tolist()]
#         labels = [d.strftime('%m/%d %H:%M') for d in hist.index]

#         return {
#             "symbol": ticker_symbol,
#             "name": query,  # 사용자가 입력한 이름 그대로 반환
#             "current": current_price,
#             "change": change,
#             "prices": prices,
#             "labels": labels
#         }

#     except Exception as e:
#         print(f"Stock Data Error ({query}): {e}")
#         return None

# # =========================================================
# # 🐜 환율 히스토리 조회 (이전 코드 유지)
# # =========================================================
# def get_exchange_history_data(code, period="1mo", start_date=None, end_date=None):
#     ticker_symbol = EXCHANGE_TICKER_MAP.get(code)
#     try:
#         if ticker_symbol:
#             ticker = yf.Ticker(ticker_symbol)
#             hist = ticker.history(period=period) if not (start_date and end_date) else ticker.history(start=start_date, end=end_date)
#             if not hist.empty:
#                 return [{'date': d.strftime('%Y-%m-%d'), 'rate': round(float(r)*100 if '(100)' in code else float(r), 2)} for d, r in hist['Close'].items()]

#         # 크로스 환율 계산 (직접 티커 없을 때)
#         usd_krw = yf.Ticker("KRW=X").history(period=period)
#         clean_code = code.split('(')[0]
#         usd_target = yf.Ticker(f"{clean_code}=X").history(period=period)
        
#         if usd_krw.empty or usd_target.empty: return []
        
#         # 타임존 제거 후 병합
#         usd_krw.index = usd_krw.index.tz_localize(None)
#         usd_target.index = usd_target.index.tz_localize(None)
        
#         merged = pd.merge(usd_krw[['Close']], usd_target[['Close']], left_index=True, right_index=True, suffixes=('_krw', '_target'))
        
#         data = []
#         for d, r in merged.iterrows():
#             rate = r['Close_krw'] / r['Close_target']
#             if '(100)' in code: rate *= 100
#             data.append({'date': d.strftime('%Y-%m-%d'), 'rate': round(rate, 2)})
#         return data

#     except Exception as e:
#         print(f"Exchange Error: {e}")
#         return []

# # =========================================================
# # 🐜 금/은 시세 조회 (이전 코드 유지)
# # =========================================================
# def get_spot_history_data(symbol_type, start_date=None, end_date=None):
#     map_code = {'GOLD': 'GC=F', 'SILVER': 'SI=F'}
#     try:
#         spot = yf.Ticker(map_code.get(symbol_type, 'GC=F'))
#         rate = yf.Ticker("USDKRW=X")
        
#         # 파라미터 체크 로직 생략 (위와 동일하게 구현)
#         # 간단하게 기간 기본값 처리
#         s_hist = spot.history(period="1mo")
#         r_hist = rate.history(period="1mo")
        
#         if s_hist.empty: return []
        
#         s_hist.index = s_hist.index.tz_localize(None)
#         r_hist.index = r_hist.index.tz_localize(None)
        
#         merged = pd.merge(s_hist[['Close']], r_hist[['Close']], left_index=True, right_index=True, suffixes=('_s', '_r'))
        
#         return [{
#             'date': d.strftime('%Y-%m-%d'),
#             'rate_usd': round(row['Close_s'], 2),
#             'rate_krw': round(row['Close_s'] * row['Close_r'], 0)
#         } for d, row in merged.iterrows()]
#     except: return []

# # 더미 함수 (사용 안함)
# def get_krx_mapping(): pass