import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pykrx import stock

# =========================================================
# 1. 매핑 데이터 (유지)
# =========================================================
EXCHANGE_TICKER_MAP = {
    'USD': 'KRW=X', 'EUR': 'EURKRW=X', 'JPY(100)': 'JPYKRW=X',
    'CNH': 'CNYKRW=X', 'GBP': 'GBPKRW=X', 'HKD': 'HKDKRW=X',
    'SGD': 'SGDKRW=X', 'CAD': 'CADKRW=X', 'CHF': 'CHFKRW=X',
    'AUD': 'AUDKRW=X', 'NZD': 'NZDKRW=X',
}

MARKET_TICKER_MAP = {
    "NASDAQ": "^IXIC", "S&P 500": "^GSPC", "KOSPI": "^KS11",
    "KOSDAQ": "^KQ11", "USD/KRW": "USDKRW=X", "GOLD": "GC=F",
    "HSI": "^HSI", "Nikkei 225": "^N225", "Euro Stoxx 50": "^STOXX50E"
}

KOREAN_POPULAR_MAP = {
    "삼성전자": "005930.KS", "SK하이닉스": "000660.KS", "LG에너지솔루션": "373220.KS",
    "현대차": "005380.KS", "기아": "000270.KS", "네이버": "035420.KS", "카카오": "035720.KS",
    "에코프로": "086520.KQ", "에코프로비엠": "247540.KQ", "알테오젠": "196170.KQ",
    "애플": "AAPL", "테슬라": "TSLA", "엔비디아": "NVDA", "마이크로소프트": "MSFT",
    "구글": "GOOGL", "아마존": "AMZN", "메타": "META", "넷플릭스": "NFLX",
    "로켓랩": "RKLB", "아이온큐": "IONQ", "팔란티어": "PLTR", "비트코인": "BTC-USD"
}

_KRX_TICKER_CACHE = {}

# =========================================================
# 2. 유틸리티 함수 (유지)
# =========================================================
def get_latest_valid_date():
    for i in range(10):
        check_date = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
        try:
            df = stock.get_market_ohlcv(check_date, check_date, "005930")
            if not df.empty and df['거래량'].iloc[0] > 0: return check_date
        except: continue
    return datetime.now().strftime("%Y%m%d")

def get_krx_mapping():
    global _KRX_TICKER_CACHE
    if len(_KRX_TICKER_CACHE) > 500: return _KRX_TICKER_CACHE
    try:
        target_date = get_latest_valid_date()
        new_cache = {}
        for ticker in stock.get_market_ticker_list(target_date, market="KOSPI"):
            new_cache[stock.get_market_ticker_name(ticker)] = f"{ticker}.KS"
        for ticker in stock.get_market_ticker_list(target_date, market="KOSDAQ"):
            new_cache[stock.get_market_ticker_name(ticker)] = f"{ticker}.KQ"
        if new_cache:
            _KRX_TICKER_CACHE = new_cache
            _KRX_TICKER_CACHE.update(KOREAN_POPULAR_MAP)
        return _KRX_TICKER_CACHE
    except: return KOREAN_POPULAR_MAP

def get_global_market_data():
    results = {}
    for name, symbol in MARKET_TICKER_MAP.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="7d")
            if not hist.empty and len(hist) >= 2:
                curr, prev = hist['Close'].iloc[-1], hist['Close'].iloc[-2]
                change, rate = curr - prev, ((curr - prev) / prev) * 100
                results[name] = {
                    "value": f"{curr:,.2f}", "change": f"{change:+.2f}",
                    "rate": f"{rate:+.2f}%", "isUp": change > 0, "symbol": symbol
                }
        except: results[name] = None
    return results

def search_ticker_from_yahoo(keyword):
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'q': keyword, 'quotesCount': 1, 'newsCount': 0}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=3)
        data = res.json()
        if 'quotes' in data and len(data['quotes']) > 0:
            return data['quotes'][0]['symbol']
    except: pass
    return None

# =========================================================
# 3. 핵심: 주식 상세 조회 (봉차트 지원 업그레이드)
# =========================================================
def get_stock_data(query, period="1d", start_date=None, end_date=None):
    query = query.strip()
    ticker_symbol = None
    
    krx_map = get_krx_mapping()
    if query in KOREAN_POPULAR_MAP: ticker_symbol = KOREAN_POPULAR_MAP[query]
    elif query in krx_map: ticker_symbol = krx_map[query]
    elif query in MARKET_TICKER_MAP.values(): ticker_symbol = query
    elif not query.replace('.','').isdigit() and not query.encode().isalpha():
        candidates = [name for name in krx_map.keys() if query in name]
        if candidates: ticker_symbol = krx_map[sorted(candidates, key=len)[0]]
    
    if not ticker_symbol:
        ticker_symbol = f"{query}.KS" if query.isdigit() else query.upper()

    # 🐜 [기간 설정 로직 개선]
    # 사용자가 'day'(일봉), 'week'(주봉), 'month'(월봉)을 요청하면 그에 맞춰 설정
    yf_params = {"period": "1d", "interval": "5m"} # 기본값 (당일 분봉)

    if period == "day":   yf_params = {"period": "1y", "interval": "1d"}   # 일봉
    elif period == "week":  yf_params = {"period": "2y", "interval": "1wk"}  # 주봉
    elif period == "month": yf_params = {"period": "5y", "interval": "1mo"}  # 월봉
    elif period == "1d":    yf_params = {"period": "1d", "interval": "5m"}   # 당일 (5일치 가져와서 자름)
    
    def fetch_data(symbol):
        ticker = yf.Ticker(symbol)
        try:
            # period가 1d(당일)일 경우, 장 시작 직후 데이터가 없을 수 있으므로 넉넉히 5d를 가져와서 오늘 것만 필터링
            if period == "1d":
                return ticker.history(period="5d", interval="5m")
            
            if start_date and end_date:
                return ticker.history(start=start_date, end=end_date, interval=yf_params['interval'])
            return ticker.history(period=yf_params['period'], interval=yf_params['interval'])
        except: return pd.DataFrame()

    hist = fetch_data(ticker_symbol)

    if hist.empty and query.encode().isalpha():
        found_symbol = search_ticker_from_yahoo(query)
        if found_symbol and found_symbol != ticker_symbol:
            ticker_symbol = found_symbol
            hist = fetch_data(ticker_symbol)

    if hist.empty: return None

    # [1d 필터링] 5일치 가져왔으면 오늘(마지막 날짜) 데이터만 남기기
    if period == "1d":
        last_date = hist.index[-1].date()
        hist = hist[hist.index.date == last_date]

    history_list = []
    is_kr = ticker_symbol.endswith(('.KS', '.KQ'))
    
    for dt, row in hist.iterrows():
        # 날짜 포맷 (일봉 이상은 YYYY-MM-DD, 분봉은 시간까지)
        date_str = dt.strftime('%Y-%m-%d')
        if period == '1d': 
             date_str = dt.strftime('%m/%d %H:%M') # 차트 X축용

        # 캔들스틱용 데이터 (Open, High, Low, Close)
        history_list.append({
            "date": date_str,
            "x": dt.timestamp() * 1000, # JS 타임스탬프 (차트 라이브러리용)
            "open": round(row['Open'], 0 if is_kr else 2),
            "high": round(row['High'], 0 if is_kr else 2),
            "low": round(row['Low'], 0 if is_kr else 2),
            "close": round(row['Close'], 0 if is_kr else 2),
            "volume": int(row['Volume'])
        })

    # 전일 종가 계산 (등락폭 기준용)
    prev_close = hist['Close'].iloc[0] # 기본값
    if period == "1d" and len(history_list) > 0:
        # 당일 차트의 기준은 '오늘 시가(Open)'로 잡아서 색상을 나눌 것이므로
        # 여기서는 등락률 계산을 위해 전일 종가를 가져오려 노력
        try:
            ticker = yf.Ticker(ticker_symbol)
            prev_close = ticker.info.get('previousClose', history_list[0]['open'])
        except: 
            prev_close = history_list[0]['open']

    return {
        "symbol": ticker_symbol, 
        "name": query, 
        "currency": "KRW" if is_kr else "USD",
        "current": hist['Close'].iloc[-1],
        "change": hist['Close'].iloc[-1] - prev_close,
        "prev_close": prev_close, # 전일 종가
        "history": history_list
    }

# (나머지 exchange, spot 함수는 그대로 두시면 됩니다)
def get_exchange_history_data(code, period="1mo", start_date=None, end_date=None):
    ticker_symbol = EXCHANGE_TICKER_MAP.get(code)
    try:
        if ticker_symbol:
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period=period) if not (start_date and end_date) else ticker.history(start=start_date, end=end_date)
            if not hist.empty:
                return [{'date': d.strftime('%Y-%m-%d'), 'rate': round(float(r)*100 if '(100)' in code else float(r), 2)} for d, r in hist['Close'].items()]
        return [] 
    except: return []

def get_spot_history_data(symbol_type, start_date=None, end_date=None):
    map_code = {'GOLD': 'GC=F', 'SILVER': 'SI=F'}
    try:
        spot = yf.Ticker(map_code.get(symbol_type, 'GC=F'))
        rate = yf.Ticker("USDKRW=X")
        s_hist = spot.history(period="1mo" if not start_date else None, start=start_date, end=end_date)
        r_hist = rate.history(period="1mo" if not start_date else None, start=start_date, end=end_date)
        if s_hist.empty: return [] 
        s_hist.index = s_hist.index.tz_localize(None)
        r_hist.index = r_hist.index.tz_localize(None)
        merged = pd.merge(s_hist[['Close']], r_hist[['Close']], left_index=True, right_index=True, how='outer', suffixes=('_s', '_r')).ffill().dropna()
        if not start_date: merged = merged.tail(30)
        return [{'date': d.strftime('%Y-%m-%d'), 'rate_usd': round(row['Close_s'], 2), 'rate_krw': round(row['Close_s'] * row['Close_r'], 0)} for d, row in merged.iterrows()]
    except: return []
    
# 1/13까지
# import requests
# import yfinance as yf
# import pandas as pd
# from datetime import datetime, timedelta
# from pykrx import stock

# # =========================================================
# # 1. 매핑 데이터 (한국어 편의성 & 속도 최적화용)
# # =========================================================
# EXCHANGE_TICKER_MAP = {
#     'USD': 'KRW=X', 'EUR': 'EURKRW=X', 'JPY(100)': 'JPYKRW=X',
#     'CNH': 'CNYKRW=X', 'GBP': 'GBPKRW=X', 'HKD': 'HKDKRW=X',
#     'SGD': 'SGDKRW=X', 'CAD': 'CADKRW=X', 'CHF': 'CHFKRW=X',
#     'AUD': 'AUDKRW=X', 'NZD': 'NZDKRW=X',
# }

# MARKET_TICKER_MAP = {
#     "NASDAQ": "^IXIC", "S&P 500": "^GSPC", "KOSPI": "^KS11",
#     "KOSDAQ": "^KQ11", "USD/KRW": "USDKRW=X", "GOLD": "GC=F",
#     "HSI": "^HSI", "Nikkei 225": "^N225", "Euro Stoxx 50": "^STOXX50E"
# }

# # 자주 찾는 종목 하드코딩 (속도 향상용)
# KOREAN_POPULAR_MAP = {
#     "삼성전자": "005930.KS", "SK하이닉스": "000660.KS", "LG에너지솔루션": "373220.KS",
#     "현대차": "005380.KS", "기아": "000270.KS", "네이버": "035420.KS", "카카오": "035720.KS",
#     "에코프로": "086520.KQ", "에코프로비엠": "247540.KQ", "알테오젠": "196170.KQ",
#     "애플": "AAPL", "테슬라": "TSLA", "엔비디아": "NVDA", "마이크로소프트": "MSFT",
#     "구글": "GOOGL", "아마존": "AMZN", "메타": "META", "넷플릭스": "NFLX",
#     "로켓랩": "RKLB", "아이온큐": "IONQ", "팔란티어": "PLTR", "비트코인": "BTC-USD"
# }

# _KRX_TICKER_CACHE = {}

# # =========================================================
# # 2. 유틸리티 함수
# # =========================================================
# def get_latest_valid_date():
#     """데이터가 확실히 존재하는 최근 영업일을 역추적"""
#     for i in range(10):
#         check_date = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
#         try:
#             df = stock.get_market_ohlcv(check_date, check_date, "005930")
#             if not df.empty and df['거래량'].iloc[0] > 0:
#                 return check_date
#         except: continue
#     return datetime.now().strftime("%Y%m%d")

# def get_krx_mapping():
#     """국내 종목 심볼 매핑 (캐싱)"""
#     global _KRX_TICKER_CACHE
#     if len(_KRX_TICKER_CACHE) > 500: return _KRX_TICKER_CACHE
#     try:
#         target_date = get_latest_valid_date()
#         new_cache = {}
#         for ticker in stock.get_market_ticker_list(target_date, market="KOSPI"):
#             new_cache[stock.get_market_ticker_name(ticker)] = f"{ticker}.KS"
#         for ticker in stock.get_market_ticker_list(target_date, market="KOSDAQ"):
#             new_cache[stock.get_market_ticker_name(ticker)] = f"{ticker}.KQ"
        
#         if new_cache:
#             _KRX_TICKER_CACHE = new_cache
#             _KRX_TICKER_CACHE.update(KOREAN_POPULAR_MAP) # 인기종목 우선순위
#         return _KRX_TICKER_CACHE
#     except: return KOREAN_POPULAR_MAP

# def get_global_market_data():
#     """홈 화면용 글로벌 지수"""
#     results = {}
#     for name, symbol in MARKET_TICKER_MAP.items():
#         try:
#             ticker = yf.Ticker(symbol)
#             hist = ticker.history(period="7d")
#             if not hist.empty and len(hist) >= 2:
#                 curr, prev = hist['Close'].iloc[-1], hist['Close'].iloc[-2]
#                 change, rate = curr - prev, ((curr - prev) / prev) * 100
#                 results[name] = {
#                     "value": f"{curr:,.2f}", "change": f"{change:+.2f}",
#                     "rate": f"{rate:+.2f}%", "isUp": change > 0, "symbol": symbol
#                 }
#         except: results[name] = None
#     return results

# # 🐜 [New] 야후 파이낸스 검색 API (이름 -> 티커 변환기)
# def search_ticker_from_yahoo(keyword):
#     """
#     'apple' -> 'AAPL', 'rocket lab' -> 'RKLB' 처럼
#     영어 이름을 실제 티커로 찾아주는 함수
#     """
#     url = "https://query2.finance.yahoo.com/v1/finance/search"
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     params = {'q': keyword, 'quotesCount': 1, 'newsCount': 0}
    
#     try:
#         res = requests.get(url, headers=headers, params=params, timeout=3)
#         data = res.json()
#         if 'quotes' in data and len(data['quotes']) > 0:
#             found_symbol = data['quotes'][0]['symbol'] # 가장 정확도 높은 1개 리턴
#             print(f"🔍 [Yahoo Auto-Search] '{keyword}' -> Found: {found_symbol}")
#             return found_symbol
#     except Exception as e:
#         print(f"Search API Error: {e}")
#     return None

# # =========================================================
# # 3. 핵심: 주식 상세 조회 (3단계 검색 적용)
# # =========================================================
# def get_stock_data(query, period="1d", start_date=None, end_date=None):
#     query = query.strip()
#     ticker_symbol = None
    
#     # [1단계] 미리 정의된 맵에서 찾기
#     krx_map = get_krx_mapping()
#     if query in KOREAN_POPULAR_MAP: ticker_symbol = KOREAN_POPULAR_MAP[query]
#     elif query in krx_map: ticker_symbol = krx_map[query]
#     elif query in MARKET_TICKER_MAP.values(): ticker_symbol = query
#     elif not query.replace('.','').isdigit() and not query.encode().isalpha():
#         # 한글 유사 검색
#         candidates = [name for name in krx_map.keys() if query in name]
#         if candidates: ticker_symbol = krx_map[sorted(candidates, key=len)[0]]
    
#     # [2단계] 맵에 없으면, 일단 입력값 그대로 티커로 간주 (RKLB, AAPL 등)
#     if not ticker_symbol:
#         ticker_symbol = f"{query}.KS" if query.isdigit() else query.upper()

#     # 데이터 가져오기 시도 함수
#     def fetch_data(symbol):
#         ticker = yf.Ticker(symbol)
#         # 기간 설정 (1d -> 5d 자동 확장 로직 포함)
#         search_period = "5d" if period == "1d" else period
#         interval = "5m" if period == "1d" else "1d"
#         if start_date and end_date: interval = "1d"
        
#         if start_date and end_date:
#             return ticker.history(start=start_date, end=end_date, interval="1d")
#         else:
#             return ticker.history(period=search_period, interval=interval)

#     # 1차 시도
#     hist = fetch_data(ticker_symbol)

#     # 🐜 [3단계] 데이터가 없고, 영문 입력이라면 -> 야후 검색 API로 진짜 티커 찾기
#     if hist.empty and query.encode().isalpha():
#         print(f"⚠️ '{ticker_symbol}' 데이터 없음. 야후 검색 API 시도...")
#         found_symbol = search_ticker_from_yahoo(query)
#         if found_symbol and found_symbol != ticker_symbol:
#             ticker_symbol = found_symbol
#             hist = fetch_data(ticker_symbol) # 찾은 티커로 재시도

#     if hist.empty: return None

#     # 데이터 가공 (1d 필터링 등)
#     if period == "1d":
#         last_date = hist.index[-1].date()
#         hist = hist[hist.index.date == last_date]

#     history_list = []
#     is_kr = ticker_symbol.endswith(('.KS', '.KQ'))
#     for dt, row in hist.iterrows():
#         history_list.append({
#             "date": dt.strftime('%Y-%m-%d') if period != '1d' and not (start_date and end_date) else dt.strftime('%m/%d %H:%M'),
#             "close": round(row['Close'], 0 if is_kr else 2),
#             "volume": int(row['Volume'])
#         })

#     # history_list가 비어있으면(장전 등) 마지막 데이터 하나라도 넣기
#     if not history_list and not hist.empty:
#          row = hist.iloc[-1]
#          history_list.append({
#             "date": hist.index[-1].strftime('%m/%d %H:%M'),
#             "close": round(row['Close'], 0 if is_kr else 2),
#             "volume": int(row['Volume'])
#         })

#     return {
#         "symbol": ticker_symbol, "name": query, 
#         "current": hist['Close'].iloc[-1],
#         "change": hist['Close'].iloc[-1] - hist['Close'].iloc[0],
#         "currency": "KRW" if is_kr else "USD",
#         "history": history_list
#     }

# # (환율, 금 시세 함수는 기존 유지)
# def get_exchange_history_data(code, period="1mo", start_date=None, end_date=None):
#     ticker_symbol = EXCHANGE_TICKER_MAP.get(code)
#     try:
#         if ticker_symbol:
#             ticker = yf.Ticker(ticker_symbol)
#             hist = ticker.history(period=period) if not (start_date and end_date) else ticker.history(start=start_date, end=end_date)
#             if not hist.empty:
#                 return [{'date': d.strftime('%Y-%m-%d'), 'rate': round(float(r)*100 if '(100)' in code else float(r), 2)} for d, r in hist['Close'].items()]
#         return [] 
#     except: return []

# def get_spot_history_data(symbol_type, start_date=None, end_date=None):
#     map_code = {'GOLD': 'GC=F', 'SILVER': 'SI=F'}
#     try:
#         spot = yf.Ticker(map_code.get(symbol_type, 'GC=F'))
#         rate = yf.Ticker("USDKRW=X")
#         s_hist = spot.history(period="1mo" if not start_date else None, start=start_date, end=end_date)
#         r_hist = rate.history(period="1mo" if not start_date else None, start=start_date, end=end_date)
#         if s_hist.empty: return [] 
#         s_hist.index = s_hist.index.tz_localize(None)
#         r_hist.index = r_hist.index.tz_localize(None)
#         merged = pd.merge(s_hist[['Close']], r_hist[['Close']], left_index=True, right_index=True, how='outer', suffixes=('_s', '_r')).ffill().dropna()
#         if not start_date: merged = merged.tail(30)
#         return [{'date': d.strftime('%Y-%m-%d'), 'rate_usd': round(row['Close_s'], 2), 'rate_krw': round(row['Close_s'] * row['Close_r'], 0)} for d, row in merged.iterrows()]
#     except: return []
#-----------------------------------------------------------------------------------------------------
# import yfinance as yf
# import pandas as pd
# from datetime import datetime, timedelta
# from pykrx import stock

# # 1. 환율 매핑
# EXCHANGE_TICKER_MAP = {
#     'USD': 'KRW=X', 'EUR': 'EURKRW=X', 'JPY(100)': 'JPYKRW=X',
#     'CNH': 'CNYKRW=X', 'GBP': 'GBPKRW=X', 'HKD': 'HKDKRW=X',
#     'SGD': 'SGDKRW=X', 'CAD': 'CADKRW=X', 'CHF': 'CHFKRW=X',
#     'AUD': 'AUDKRW=X', 'NZD': 'NZDKRW=X',
# }

# # 2. 글로벌 지수 매핑
# MARKET_TICKER_MAP = {
#     "NASDAQ": "^IXIC", "S&P 500": "^GSPC", "KOSPI": "^KS11",
#     "KOSDAQ": "^KQ11", "USD/KRW": "USDKRW=X", "GOLD": "GC=F",
#     "HSI": "^HSI", "Nikkei 225": "^N225", "Euro Stoxx 50": "^STOXX50E"
# }

# # 3. 미국 인기 주식 매핑
# US_STOCK_MAP = {
#     "애플": "AAPL", "마이크로소프트": "MSFT", "엔비디아": "NVDA",
#     "구글": "GOOGL", "아마존": "AMZN", "메타": "META", "테슬라": "TSLA",
#     "TSMC": "TSM", "AMD": "AMD", "인텔": "INTC", "마이크론": "MU",
#     "브로드컴": "AVGO", "퀄컴": "QCOM", "ARM": "ARM", "슈퍼마이크로": "SMCI",
#     "스타벅스": "SBUX", "코카콜라": "KO", "맥도날드": "MCD", "나이키": "NKE",
#     "넷플릭스": "NFLX", "디즈니": "DIS", "코스트코": "COST", "월마트": "WMT",
#     "화이자": "PFE", "모더나": "MRNA", "보잉": "BA", "에어비앤비": "ABNB",
#     "쿠팡": "CPNG", "로블록스": "RBLX", "팔란티어": "PLTR", "코인베이스": "COIN",
#     "QQQ": "QQQ", "SPY": "SPY", "VOO": "VOO", "SOXX": "SOXX", "TQQQ": "TQQQ", 
#     "SOXL": "SOXL", "SQQQ": "SQQQ", "SOXS": "SOXS", "NVDL": "NVDL", "TSLL": "TSLL"
# }

# # 🐜 4. [추가] 한국 인기 종목 안전장치 (pykrx 실패 대비용)
# KOREAN_POPULAR_MAP = {
#     "삼성전자": "005930.KS", "SK하이닉스": "000660.KS", "LG에너지솔루션": "373220.KS",
#     "삼성바이오로직스": "207940.KS", "현대차": "005380.KS", "기아": "000270.KS",
#     "셀트리온": "068270.KS", "KB금융": "105560.KS", "네이버": "035420.KS", "NAVER": "035420.KS",
#     "카카오": "035720.KS", "POSCO홀딩스": "005490.KS", "삼성SDI": "006400.KS",
#     "LG화학": "051910.KS", "현대모비스": "012330.KS", "신한지주": "055550.KS",
#     "에코프로": "086520.KQ", "에코프로비엠": "247540.KQ", "알테오젠": "196170.KQ"
# }

# _KRX_TICKER_CACHE = {}

# def get_latest_valid_date():
#     """데이터가 확실히 존재하는 최근 영업일을 역추적"""
#     for i in range(10):
#         check_date = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
#         try:
#             df = stock.get_market_ohlcv(check_date, check_date, "005930")
#             if not df.empty and df['거래량'].iloc[0] > 0:
#                 return check_date
#         except: continue
#     return datetime.now().strftime("%Y%m%d")

# def get_krx_mapping():
#     """국내 종목 심볼 매핑"""
#     global _KRX_TICKER_CACHE
#     if len(_KRX_TICKER_CACHE) > 500: return _KRX_TICKER_CACHE
    
#     try:
#         target_date = get_latest_valid_date()
#         new_cache = {}
#         # KOSPI
#         for ticker in stock.get_market_ticker_list(target_date, market="KOSPI"):
#             new_cache[stock.get_market_ticker_name(ticker)] = f"{ticker}.KS"
#         # KOSDAQ
#         for ticker in stock.get_market_ticker_list(target_date, market="KOSDAQ"):
#             new_cache[stock.get_market_ticker_name(ticker)] = f"{ticker}.KQ"
        
#         if new_cache:
#             _KRX_TICKER_CACHE = new_cache
#             # 🐜 안전장치 맵도 캐시에 병합 (우선순위 확보)
#             _KRX_TICKER_CACHE.update(KOREAN_POPULAR_MAP)
            
#         return _KRX_TICKER_CACHE
#     except: return KOREAN_POPULAR_MAP # 실패 시 인기 종목이라도 반환

# def get_global_market_data():
#     """글로벌 지표 조회"""
#     results = {}
#     for name, symbol in MARKET_TICKER_MAP.items():
#         try:
#             ticker = yf.Ticker(symbol)
#             hist = ticker.history(period="7d")
#             if not hist.empty and len(hist) >= 2:
#                 curr, prev = hist['Close'].iloc[-1], hist['Close'].iloc[-2]
#                 change, rate = curr - prev, ((curr - prev) / prev) * 100
#                 results[name] = {
#                     "value": f"{curr:,.2f}", "change": f"{change:+.2f}",
#                     "rate": f"{rate:+.2f}%", "isUp": change > 0, "symbol": symbol
#                 }
#         except: results[name] = None
#     return results

# def get_stock_data(query, period="1d", start_date=None, end_date=None):
#     """상세 주식 데이터 조회 (안전장치 적용)"""
#     query = query.strip()
#     ticker_symbol = None
    
#     # 1. 맵핑 조회 (순서: 인기종목 -> 전체맵 -> 미국주식 -> 지수)
#     krx_map = get_krx_mapping()
    
#     if query in KOREAN_POPULAR_MAP: ticker_symbol = KOREAN_POPULAR_MAP[query] # 🐜 1순위: 하드코딩 맵
#     elif query in krx_map: ticker_symbol = krx_map[query]
#     elif query in US_STOCK_MAP: ticker_symbol = US_STOCK_MAP[query]
#     elif query in MARKET_TICKER_MAP.values(): ticker_symbol = query
#     elif not query.replace('.','').isdigit() and not query.encode().isalpha():
#         # 한글인데 맵에 없으면 유사 검색 시도 (가장 짧은 매칭)
#         candidates = [name for name in krx_map.keys() if query in name]
#         if candidates: ticker_symbol = krx_map[sorted(candidates, key=len)[0]]
    
#     if not ticker_symbol:
#         ticker_symbol = f"{query}.KS" if query.isdigit() else query.upper()

#     print(f"🐜 검색어: {query} -> 티커: {ticker_symbol}") # 로그 확인용

#     try:
#         search_period = "5d" if period == "1d" else period
#         interval = "5m" if period == "1d" else "1d"
#         if start_date and end_date: interval = "1d"

#         ticker = yf.Ticker(ticker_symbol)
        
#         if start_date and end_date:
#             hist = ticker.history(start=start_date, end=end_date, interval="1d")
#         else:
#             hist = ticker.history(period=search_period, interval=interval)
        
#         # 코스닥 재시도
#         if hist.empty and ticker_symbol.endswith('.KS') and query.isdigit():
#             alt = ticker_symbol.replace('.KS', '.KQ')
#             ticker = yf.Ticker(alt)
#             hist = ticker.history(period=search_period, interval=interval)
#             if not hist.empty: ticker_symbol = alt

#         if hist.empty:
#             print(f"❌ 데이터 없음: {ticker_symbol}")
#             return None

#         if period == "1d":
#             last_date = hist.index[-1].date()
#             hist = hist[hist.index.date == last_date]

#         history_list = []
#         is_kr = ticker_symbol.endswith(('.KS', '.KQ'))
#         for dt, row in hist.iterrows():
#             history_list.append({
#                 "date": dt.strftime('%Y-%m-%d') if interval == '1d' else dt.strftime('%m/%d %H:%M'),
#                 "close": round(row['Close'], 0 if is_kr else 2),
#                 "volume": int(row['Volume'])
#             })

#         return {
#             "symbol": ticker_symbol, "name": query, 
#             "current": hist['Close'].iloc[-1],
#             "change": hist['Close'].iloc[-1] - hist['Close'].iloc[0],
#             "currency": "KRW" if is_kr else "USD",
#             "history": history_list
#         }
#     except Exception as e:
#         print(f"Stock Error: {e}")
#         return None

# # (환율, 금 시세 함수는 기존과 동일하게 유지)
# def get_exchange_history_data(code, period="1mo", start_date=None, end_date=None):
#     ticker_symbol = EXCHANGE_TICKER_MAP.get(code)
#     try:
#         if ticker_symbol:
#             ticker = yf.Ticker(ticker_symbol)
#             hist = ticker.history(period=period) if not (start_date and end_date) else ticker.history(start=start_date, end=end_date)
#             if not hist.empty:
#                 return [{'date': d.strftime('%Y-%m-%d'), 'rate': round(float(r)*100 if '(100)' in code else float(r), 2)} for d, r in hist['Close'].items()]
#         return [] 
#     except: return []

# def get_spot_history_data(symbol_type, start_date=None, end_date=None):
#     map_code = {'GOLD': 'GC=F', 'SILVER': 'SI=F'}
#     try:
#         spot = yf.Ticker(map_code.get(symbol_type, 'GC=F'))
#         rate = yf.Ticker("USDKRW=X")
#         s_hist = spot.history(period="1mo" if not start_date else None, start=start_date, end=end_date)
#         r_hist = rate.history(period="1mo" if not start_date else None, start=start_date, end=end_date)
#         if s_hist.empty: return [] 
#         s_hist.index = s_hist.index.tz_localize(None)
#         r_hist.index = r_hist.index.tz_localize(None)
#         merged = pd.merge(s_hist[['Close']], r_hist[['Close']], left_index=True, right_index=True, how='outer', suffixes=('_s', '_r')).ffill().dropna()
#         if not start_date: merged = merged.tail(30)
#         return [{'date': d.strftime('%Y-%m-%d'), 'rate_usd': round(row['Close_s'], 2), 'rate_krw': round(row['Close_s'] * row['Close_r'], 0)} for d, row in merged.iterrows()]
#     except: return []
#---------------------------------------------------------위는 되는거다

# # backend/finlife/utils/external_api.py
# # backend/finlife/utils/external_api.py
# import yfinance as yf
# import pandas as pd
# from datetime import datetime, timedelta
# from pykrx import stock

# # 1. 환율 매핑 (기존 유지)
# EXCHANGE_TICKER_MAP = {
#     'USD': 'KRW=X', 'EUR': 'EURKRW=X', 'JPY(100)': 'JPYKRW=X',
#     'CNH': 'CNYKRW=X', 'GBP': 'GBPKRW=X', 'HKD': 'HKDKRW=X',
#     'SGD': 'SGDKRW=X', 'CAD': 'CADKRW=X', 'CHF': 'CHFKRW=X',
#     'AUD': 'AUDKRW=X', 'NZD': 'NZDKRW=X',
# }

# # 2. 글로벌 지수 매핑
# MARKET_TICKER_MAP = {
#     "NASDAQ": "^IXIC", "S&P 500": "^GSPC", "KOSPI": "^KS11",
#     "KOSDAQ": "^KQ11", "USD/KRW": "USDKRW=X", "GOLD": "GC=F",
#     "HSI": "^HSI", # 홍콩 항셍
#     "Nikkei 225": "^N225", # 일본 닛케이
#     "Euro Stoxx 50": "^STOXX50E" # 유로 스톡스
# }

# # 3. 미국 인기 주식 매핑 (기존 유지)
# US_STOCK_MAP = {
#     "애플": "AAPL", "마이크로소프트": "MSFT", "엔비디아": "NVDA",
#     "구글": "GOOGL", "아마존": "AMZN", "메타": "META", "테슬라": "TSLA",
#     "TSMC": "TSM", "AMD": "AMD", "인텔": "INTC", "마이크론": "MU",
#     "브로드컴": "AVGO", "퀄컴": "QCOM", "ARM": "ARM", "슈퍼마이크로": "SMCI",
#     "스타벅스": "SBUX", "코카콜라": "KO", "맥도날드": "MCD", "나이키": "NKE",
#     "넷플릭스": "NFLX", "디즈니": "DIS", "코스트코": "COST", "월마트": "WMT",
#     "화이자": "PFE", "모더나": "MRNA", "보잉": "BA", "에어비앤비": "ABNB",
#     "쿠팡": "CPNG", "로블록스": "RBLX", "팔란티어": "PLTR", "코인베이스": "COIN",
#     "QQQ": "QQQ", "나스닥": "QQQ", "SPY": "SPY", "S&P500": "SPY", "VOO": "VOO",
#     "SOXX": "SOXX", "반도체": "SOXX", "TQQQ": "TQQQ", "SOXL": "SOXL", "속슬": "SOXL",
#     "티큐": "TQQQ", "SQQQ": "SQQQ", "SOXS": "SOXS", "엔비디아2배": "NVDL", "테슬라2배": "TSLL"
# }

# _KRX_TICKER_CACHE = {}

# # ... (get_latest_business_day, get_krx_mapping 기존 코드 유지 - 생략) ...
# def get_latest_business_day():
#     date = datetime.now()
#     while date.weekday() > 4 or (date.weekday() == 0 and date.hour < 9): date -= timedelta(days=1)
#     return date.strftime("%Y%m%d")

# def get_krx_mapping():
#     global _KRX_TICKER_CACHE
#     if _KRX_TICKER_CACHE: return _KRX_TICKER_CACHE
#     try:
#         target_date = get_latest_business_day()
#         for ticker in stock.get_market_ticker_list(target_date, market="KOSPI"):
#             _KRX_TICKER_CACHE[stock.get_market_ticker_name(ticker)] = f"{ticker}.KS"
#         for ticker in stock.get_market_ticker_list(target_date, market="KOSDAQ"):
#             _KRX_TICKER_CACHE[stock.get_market_ticker_name(ticker)] = f"{ticker}.KQ"
#         for ticker in stock.get_etf_ticker_list(target_date):
#             _KRX_TICKER_CACHE[stock.get_etf_ticker_name(ticker)] = f"{ticker}.KS"
#         return _KRX_TICKER_CACHE
#     except: return {}

# def get_global_market_data():
#     results = {}
#     for name, symbol in MARKET_TICKER_MAP.items():
#         try:
#             ticker = yf.Ticker(symbol)
#             hist = ticker.history(period="2d")
#             if not hist.empty and len(hist) >= 2:
#                 curr, prev = hist['Close'].iloc[-1], hist['Close'].iloc[-2]
#                 change = curr - prev
#                 rate = (change / prev) * 100
#                 results[name] = {
#                     "value": f"{curr:,.2f}",
#                     "change": f"{change:+.2f}",
#                     "rate": f"{rate:+.2f}%",
#                     "isUp": change > 0,
#                     "symbol": symbol # 🐜 모달에서 차트 그릴 때 필요해서 추가
#                 }
#         except: results[name] = None
#     return results

# # =========================================================
# # 🐜 [대개조] 기간/날짜별 상세 주식 데이터 조회
# # =========================================================
# def get_stock_data(query, period="1d", start_date=None, end_date=None):
#     query = query.strip()
#     ticker_symbol = None
    
#     # 1. 심볼 매핑 로직 (기존과 동일)
#     krx_map = get_krx_mapping()
#     if query in krx_map: ticker_symbol = krx_map[query]
#     elif query in US_STOCK_MAP: ticker_symbol = US_STOCK_MAP[query]
#     elif query in MARKET_TICKER_MAP.values(): ticker_symbol = query # 지수 심볼 직접 호출 시
#     elif not query.replace('.','').isdigit() and not query.encode().isalpha():
#         candidates = [name for name in krx_map.keys() if query in name]
#         if candidates: ticker_symbol = krx_map[sorted(candidates, key=len)[0]]
#     if not ticker_symbol:
#         if query.isdigit(): ticker_symbol = f"{query}.KS"
#         else: ticker_symbol = query.upper()

#     try:
#         # 2. 데이터 간격(Interval) 결정 로직 🐜
#         interval = "1d"
#         if start_date and end_date:
#             # 커스텀 기간이면 기본 1일
#             pass 
#         else:
#             # 프리셋 기간별 최적 간격
#             if period == "1d": interval = "5m"   # 하루는 5분봉
#             elif period == "5d": interval = "1h" # 일주일은 1시간봉
#             elif period in ["1mo", "3mo"]: interval = "1d"
#             elif period in ["6mo", "1y", "ytd", "max"]: interval = "1d"

#         # 3. yfinance 호출
#         ticker = yf.Ticker(ticker_symbol)
        
#         if start_date and end_date:
#             hist = ticker.history(start=start_date, end=end_date, interval="1d")
#         else:
#             hist = ticker.history(period=period, interval=interval)
        
#         # 코스닥 재시도 로직
#         if hist.empty and ticker_symbol.endswith('.KS') and query.isdigit():
#             alt = ticker_symbol.replace('.KS', '.KQ')
#             ticker = yf.Ticker(alt)
#             if start_date and end_date:
#                 hist = ticker.history(start=start_date, end=end_date, interval="1d")
#             else:
#                 hist = ticker.history(period=period, interval=interval)
#             if not hist.empty: ticker_symbol = alt

#         if hist.empty: return None

#         # 4. 데이터 가공 (표 & 차트용 리스트)
#         history_list = []
#         for dt, row in hist.iterrows():
#             close_val = row['Close']
#             # 한국 시장은 소수점 제거, 미국은 2자리
#             is_kr = ticker_symbol.endswith(('.KS', '.KQ'))
            
#             history_list.append({
#                 "date": dt.strftime('%Y-%m-%d') if interval == '1d' else dt.strftime('%m/%d %H:%M'),
#                 "close": round(close_val, 0 if is_kr else 2),
#                 "open": round(row['Open'], 0 if is_kr else 2),
#                 "high": round(row['High'], 0 if is_kr else 2),
#                 "low": round(row['Low'], 0 if is_kr else 2),
#                 "volume": int(row['Volume'])
#             })

#         # 현재가 정보 (마지막 데이터)
#         current_price = hist['Close'].iloc[-1]
#         prev_close = hist['Close'].iloc[0] # 기간 내 시초가 기준 변동
#         # *참고: 실제 전일 대비 등락은 info를 불러와야 정확하지만, 여기선 '조회 기간 내 변동'을 보여줌
        
#         return {
#             "symbol": ticker_symbol,
#             "name": query, 
#             "current": current_price,
#             "change": current_price - prev_close,
#             "currency": "KRW" if ticker_symbol.endswith(('.KS', '.KQ')) else "USD",
#             "history": history_list # 🐜 차트와 표를 그릴 핵심 데이터
#         }

#     except Exception as e:
#         print(f"Stock Error: {e}")
#         return None

# # ... (exchange, spot 함수 유지) ...
# def get_exchange_history_data(code, period="1mo", start_date=None, end_date=None):
#     # 기존 코드 그대로 유지
#     ticker_symbol = EXCHANGE_TICKER_MAP.get(code)
#     try:
#         if ticker_symbol:
#             ticker = yf.Ticker(ticker_symbol)
#             hist = ticker.history(period=period) if not (start_date and end_date) else ticker.history(start=start_date, end=end_date)
#             if not hist.empty:
#                 return [{'date': d.strftime('%Y-%m-%d'), 'rate': round(float(r)*100 if '(100)' in code else float(r), 2)} for d, r in hist['Close'].items()]

#         usd_krw = yf.Ticker("KRW=X").history(period=period)
#         clean_code = code.split('(')[0]
#         usd_target = yf.Ticker(f"{clean_code}=X").history(period=period)
        
#         if usd_krw.empty or usd_target.empty: return []
        
#         usd_krw.index = usd_krw.index.tz_localize(None)
#         usd_target.index = usd_target.index.tz_localize(None)
        
#         merged = pd.merge(usd_krw[['Close']], usd_target[['Close']], left_index=True, right_index=True, suffixes=('_krw', '_target'))
        
#         data = []
#         for d, r in merged.iterrows():
#             rate = r['Close_krw'] / r['Close_target']
#             if '(100)' in code: rate *= 100
#             data.append({'date': d.strftime('%Y-%m-%d'), 'rate': round(rate, 2)})
#         return data
#     except: return []

# def get_spot_history_data(symbol_type, start_date=None, end_date=None):
#     # 기존 코드 그대로 유지
#     map_code = {'GOLD': 'GC=F', 'SILVER': 'SI=F'}
#     try:
#         spot = yf.Ticker(map_code.get(symbol_type, 'GC=F'))
#         rate = yf.Ticker("USDKRW=X")
#         s_hist = spot.history(period="1mo")
#         r_hist = rate.history(period="1mo")
#         if s_hist.empty: return []
#         s_hist.index = s_hist.index.tz_localize(None)
#         r_hist.index = r_hist.index.tz_localize(None)
#         merged = pd.merge(s_hist[['Close']], r_hist[['Close']], left_index=True, right_index=True, suffixes=('_s', '_r'))
#         return [{'date': d.strftime('%Y-%m-%d'), 'rate_usd': round(row['Close_s'], 2), 'rate_krw': round(row['Close_s'] * row['Close_r'], 0)} for d, row in merged.iterrows()]
#     except: return []


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