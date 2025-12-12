import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pykrx import stock
from typing import Dict, List, Optional, Any

# FinanceDataReader (업종 정보용)
try:
    import FinanceDataReader as fdr
    HAS_FDR = True
except Exception:
    HAS_FDR = False

# ============== 기본 사용자 설정 ==============
CFG = {
    "w_roe": 0.40,
    "w_div": 0.30,
    "w_per": 0.15,
    "w_pbr": 0.15,
    "market": "KOSPI",
    "top_n_div": 100,
    "report_top": 20,
    "apply_sector_adjust": True,
    "include_reits": True,
    "include_financials": True,
    "exclude_pref_spac": True,
    "min_trading_value_krw": 5e8,
}
# =======================================

# -----------------------------------------------------------
# 유틸리티 함수들
# -----------------------------------------------------------

def pct_rank(s: pd.Series, higher=True) -> pd.Series:
    s = s.copy()
    pct = s.rank(pct=True, ascending=True)
    if higher: res = pct * 100
    else: res = (1 - pct) * 100
    return res.clip(0, 100)

def get_latest_bday(max_lookback_days=10, market="KOSPI"):
    today = datetime.today().date()
    if datetime.now().hour < 9:
        today = today - timedelta(days=1)
        
    for i in range(max_lookback_days):
        d = (today - timedelta(days=i)).strftime("%Y%m%d")
        try:
            df = stock.get_market_ohlcv(d, d, "005930") 
            if not df.empty:
                return d
        except Exception:
            pass
    return datetime.today().strftime("%Y%m%d")

def safe_sector_dataframe():
    if not HAS_FDR:
        return None
    try:
        krx_list = fdr.StockListing("KRX")
        rename_map = {"Symbol": "ticker", "Name": "fdr_name"}
        for k, v in rename_map.items():
            if k in krx_list.columns:
                krx_list = krx_list.rename(columns={k: v})
        
        if "ticker" in krx_list.columns:
            krx_list["ticker"] = krx_list["ticker"].astype(str).str.zfill(6)
            
        for col in ["Sector", "Industry", "Market"]:
            if col not in krx_list.columns:
                krx_list[col] = np.nan
        return krx_list.set_index("ticker")[["fdr_name", "Sector", "Industry", "Market"]]
    except Exception:
        return None

def choose_sector(row):
    for col in ["Sector", "Industry", "Market"]:
        val = row.get(col, None)
        if isinstance(val, str) and val:
            return val
    return "기타"

# -----------------------------------------------------------
# 📌 핵심 분석 엔진 (calculate_ranking_logic)
# -----------------------------------------------------------
def calculate_ranking_logic(current_cfg: Dict[str, Any]):
    
    # ✨ 디버깅 포인트: 실제로 적용되는 가중치 확인
    print(f"🐢 [1] 가중치 적용: ROE({current_cfg['w_roe']:.2f}) DIV({current_cfg['w_div']:.2f}) PER({current_cfg['w_per']:.2f}) PBR({current_cfg['w_pbr']:.2f})")
    
    BASE_DATE = get_latest_bday(market=current_cfg["market"])

    # 1) 기본 재무
    try:
        fund = stock.get_market_fundamental_by_ticker(BASE_DATE, market=current_cfg["market"]).copy()
    except:
        return BASE_DATE, pd.DataFrame() 

    # ... (중략: 데이터 수집 및 필터링) ...
    need_cols = ["PER", "PBR", "EPS", "BPS", "DPS", "DIV"]
    for col in need_cols:
        if col not in fund.columns:
            fund[col] = np.nan

    fund = fund.replace([np.inf, -np.inf], np.nan)
    fund["DPS"] = fund["DPS"].fillna(0)
    fund["EPS"] = fund["EPS"].fillna(0)

    # 2) 시총 / 거래대금
    cap = stock.get_market_cap_by_ticker(BASE_DATE, market=current_cfg["market"]).copy()
    if "거래대금" not in cap.columns: cap["거래대금"] = np.nan
    df = fund.join(cap[["거래대금", "상장주식수"]] if "상장주식수" in cap.columns else cap[["거래대금"]], how="left")

    # 3) 종목명 / 섹터
    tickers = df.index.tolist()
    name_map = {t: stock.get_market_ticker_name(t) for t in tickers}
    df["name"] = df.index.map(name_map.get)

    meta = safe_sector_dataframe()
    if meta is not None: df = df.join(meta, how="left")
    else: df["Sector"] = np.nan

    df["Sector"] = df.apply(choose_sector, axis=1)

    # 4) 필터링
    if current_cfg["exclude_pref_spac"]:
        name_series = df["name"].fillna("")
        df = df[~name_series.str.endswith("우")]
        df = df[~name_series.str.contains("우선|스팩|SPAC")]

    if not current_cfg["include_reits"]:
        df = df[~df.apply(lambda r: "리츠" in (r["name"] or "") or "REIT" in (r["Sector"] or ""), axis=1)]

    if not current_cfg["include_financials"]:
        df = df[~df["Sector"].fillna("").apply(lambda x: any(k in x for k in ["은행", "증권", "보험", "지주", "금융"]))]

    # 5) ROE 근사
    df["ROE_est"] = np.where((df["BPS"] > 0) & df["EPS"].notna(), df["EPS"] / df["BPS"] * 100, np.nan)

    # 6) 배당상위 N
    df_top = df.sort_values("DIV", ascending=False).head(current_cfg["top_n_div"]).copy()
    if df_top.empty: return BASE_DATE, df_top
    df_top["fcf_coverage"] = np.nan

    # 7) 백분위 점수 계산 (전체)
    df_top["div_pct_all"] = pct_rank(df_top["DIV"], True)
    df_top["roe_pct_all"] = pct_rank(df_top["ROE_est"], True)
    df_top["per_pct_all"] = pct_rank(df_top["PER"], False) 
    df_top["pbr_pct_all"] = pct_rank(df_top["PBR"], False) 

    # 8) 섹터 조정
    if current_cfg["apply_sector_adjust"]:
        def grp_pct(col, higher=True):
            return df_top.groupby("Sector")[col].transform(lambda s: pct_rank(s, higher=higher))

        df_top["div_pct"] = grp_pct("DIV", True)
        df_top["roe_pct"] = grp_pct("ROE_est", True)
        df_top["per_pct"] = grp_pct("PER", False)
        df_top["pbr_pct"] = grp_pct("PBR", False)

        grp_size = df_top.groupby("Sector")["name"].transform("size")
        small_grp = grp_size < 3
        for c_pair in [("div_pct", "div_pct_all"), ("roe_pct", "roe_pct_all"), ("per_pct", "per_pct_all"), ("pbr_pct", "pbr_pct_all")]:
            df_top.loc[small_grp, c_pair[0]] = df_top.loc[small_grp, c_pair[1]]
    else:
        df_top["div_pct"] = df_top["div_pct_all"]
        df_top["roe_pct"] = df_top["roe_pct_all"]
        df_top["per_pct"] = df_top["per_pct_all"]
        df_top["pbr_pct"] = df_top["pbr_pct_all"]

    # 9) 최종 점수 ✨ [핵심] 수신된 가중치로 계산
    df_top["base_score"] = (
        current_cfg["w_roe"] * df_top["roe_pct"] +
        current_cfg["w_div"] * df_top["div_pct"] +
        current_cfg["w_per"] * df_top["per_pct"] +
        current_cfg["w_pbr"] * df_top["pbr_pct"]
    )

    df_top["score"] = df_top["base_score"]

    # PER, PBR 이상치 제거
    df_top = df_top[df_top["PER"] > 0]
    df_top = df_top[df_top["PBR"] > 0]

    # 티커 정리
    df_top["ticker"] = df_top.index.astype(str).str.zfill(6)

    ranked = df_top.sort_values("score", ascending=False).reset_index(drop=True)
    ranked["score"] = ranked["score"].round(2)

    TOP_N = int(current_cfg["report_top"])
    disp_cols = ["ticker", "name", "score", "DIV", "ROE_est", "PER", "PBR", "Sector"]
    disp_cols = [c for c in disp_cols if c in ranked.columns]

    return BASE_DATE, ranked[disp_cols].head(TOP_N)


# ================================
# ✅ API 호출용 래퍼 함수 (views.py가 이걸 부름)
# ================================
def get_stock_ranking(limit: Optional[int] = None, weights: Optional[Dict[str, float]] = None) -> Dict[str, object]:
    
    current_cfg = CFG.copy()
    if weights:
        for k, v in weights.items():
            if k in current_cfg:
                current_cfg[k] = v 
    
    try:
        base_date, df = calculate_ranking_logic(current_cfg)

        if df is None or df.empty:
            print("🚨 [Alert] 분석된 종목이 없습니다.")
            return {"base_date": base_date, "rows": []}

        if limit:
            df = df.head(limit)

        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(0) 
        
        rows = df.to_dict(orient="records")
        
        print(f"✅ [Success] {len(rows)}개 종목 분석 및 변환 완료!")
        
        return {
            "base_date": base_date,
            "rows": rows,
        }

    except Exception as e:
        print(f"🔥 [Error] utils.py 실행 중 오류: {e}")
        return {"base_date": datetime.today().strftime("%Y%m%d"), "rows": []}


# import os
# from datetime import datetime, timedelta
# import numpy as np
# import pandas as pd
# from pykrx import stock
# from typing import Dict, List, Optional, Any

# # FinanceDataReader (업종 정보용)
# try:
#     import FinanceDataReader as fdr
#     HAS_FDR = True
# except Exception:
#     HAS_FDR = False

# # ============== 기본 사용자 설정 ==============
# CFG = {
#     "w_roe": 0.40,
#     "w_div": 0.30,
#     "w_per": 0.15,
#     "w_pbr": 0.15,
#     "market": "KOSPI",
#     "top_n_div": 100,
#     "report_top": 20,
#     "apply_sector_adjust": True,
#     "include_reits": True,
#     "include_financials": True,
#     "exclude_pref_spac": True,
#     "min_trading_value_krw": 5e8,
# }
# # =======================================

# # -----------------------------------------------------------
# # 유틸리티 함수들 (기존과 동일)
# # -----------------------------------------------------------

# def pct_rank(s: pd.Series, higher=True) -> pd.Series:
#     s = s.copy()
#     pct = s.rank(pct=True, ascending=True)
#     if higher: res = pct * 100
#     else: res = (1 - pct) * 100
#     return res.clip(0, 100)

# def get_latest_bday(max_lookback_days=10, market="KOSPI"):
#     today = datetime.today().date()
#     # 장 시작 전(9시 이전)이면 어제 날짜부터 탐색 시작
#     if datetime.now().hour < 9:
#         today = today - timedelta(days=1)
        
#     for i in range(max_lookback_days):
#         d = (today - timedelta(days=i)).strftime("%Y%m%d")
#         try:
#             # 유효한 날짜인지 체크
#             df = stock.get_market_ohlcv(d, d, "005930") 
#             if not df.empty:
#                 return d
#         except Exception:
#             pass
#     return datetime.today().strftime("%Y%m%d")

# def safe_sector_dataframe():
#     if not HAS_FDR:
#         return None
#     try:
#         krx_list = fdr.StockListing("KRX")
#         rename_map = {"Symbol": "ticker", "Name": "fdr_name"}
#         for k, v in rename_map.items():
#             if k in krx_list.columns:
#                 krx_list = krx_list.rename(columns={k: v})
        
#         if "ticker" in krx_list.columns:
#             krx_list["ticker"] = krx_list["ticker"].astype(str).str.zfill(6)
            
#         for col in ["Sector", "Industry", "Market"]:
#             if col not in krx_list.columns:
#                 krx_list[col] = np.nan
#         return krx_list.set_index("ticker")[["fdr_name", "Sector", "Industry", "Market"]]
#     except Exception:
#         return None

# def choose_sector(row):
#     for col in ["Sector", "Industry", "Market"]:
#         val = row.get(col, None)
#         if isinstance(val, str) and val:
#             return val
#     return "기타"

# # -----------------------------------------------------------
# # 📌 핵심 분석 엔진 (get_dividend_ranking)
# # -----------------------------------------------------------
# def calculate_ranking_logic(current_cfg: Dict[str, Any]):
#     print(f"🐢 [1] 가중치 적용: ROE({current_cfg['w_roe']}) DIV({current_cfg['w_div']})")
    
#     BASE_DATE = get_latest_bday(market=current_cfg["market"])

#     # 1) 기본 재무
#     try:
#         fund = stock.get_market_fundamental_by_ticker(BASE_DATE, market=current_cfg["market"]).copy()
#     except:
#         return BASE_DATE, pd.DataFrame() # 데이터 수집 실패 시

#     # ... (기존 로직 유지) ...
#     need_cols = ["PER", "PBR", "EPS", "BPS", "DPS", "DIV"]
#     for col in need_cols:
#         if col not in fund.columns:
#             fund[col] = np.nan

#     fund = fund.replace([np.inf, -np.inf], np.nan)
#     fund["DPS"] = fund["DPS"].fillna(0)
#     fund["EPS"] = fund["EPS"].fillna(0)

#     # 2) 시총 / 거래대금
#     cap = stock.get_market_cap_by_ticker(BASE_DATE, market=current_cfg["market"]).copy()
#     if "거래대금" not in cap.columns:
#         cap["거래대금"] = np.nan

#     if "상장주식수" in cap.columns:
#         df = fund.join(cap[["거래대금", "상장주식수"]], how="left")
#     else:
#         df = fund.join(cap[["거래대금"]], how="left")

#     # 3) 종목명 / 섹터
#     tickers = df.index.tolist()
#     name_map = {t: stock.get_market_ticker_name(t) for t in tickers}
#     df["name"] = df.index.map(name_map.get)

#     meta = safe_sector_dataframe()
#     if meta is not None:
#         df = df.join(meta, how="left")
#     else:
#         df["Sector"] = np.nan

#     df["Sector"] = df.apply(choose_sector, axis=1)

#     # 4) 필터링 (거래대금 필터는 주석 처리하여 데이터 나오게 함)
#     if current_cfg["exclude_pref_spac"]:
#         name_series = df["name"].fillna("")
#         df = df[~name_series.str.endswith("우")]
#         df = df[~name_series.str.contains("우선|스팩|SPAC")]

#     if not current_cfg["include_reits"]:
#         df = df[~df.apply(lambda r: "리츠" in (r["name"] or "") or "REIT" in (r["Sector"] or ""), axis=1)]

#     if not current_cfg["include_financials"]:
#         df = df[~df["Sector"].fillna("").apply(lambda x: any(k in x for k in ["은행", "증권", "보험", "지주", "금융"]))]

#     # df = df[df["거래대금"].fillna(0) >= current_cfg["min_trading_value_krw"]].copy() # 🚨 거래대금 필터링 주석 처리

#     # 5) ROE 근사
#     df["ROE_est"] = np.where((df["BPS"] > 0) & df["EPS"].notna(), df["EPS"] / df["BPS"] * 100, np.nan)

#     # 6) 배당상위 N
#     df_top = df.sort_values("DIV", ascending=False).head(current_cfg["top_n_div"]).copy()
#     df_top["fcf_coverage"] = np.nan

#     # 7) 백분위 점수 계산 (전체)
#     df_top["div_pct_all"] = pct_rank(df_top["DIV"], True)
#     df_top["roe_pct_all"] = pct_rank(df_top["ROE_est"], True)
#     df_top["per_pct_all"] = pct_rank(df_top["PER"], False) # 저PER 선호
#     df_top["pbr_pct_all"] = pct_rank(df_top["PBR"], False) # 저PBR 선호

#     # 8) 섹터 조정
#     if current_cfg["apply_sector_adjust"]:

#         def grp_pct(col, higher=True):
#             return df_top.groupby("Sector")[col].transform(lambda s: pct_rank(s, higher=higher))

#         df_top["div_pct"] = grp_pct("DIV", True)
#         df_top["roe_pct"] = grp_pct("ROE_est", True)
#         df_top["per_pct"] = grp_pct("PER", False)
#         df_top["pbr_pct"] = grp_pct("PBR", False)

#         # 섹터 내 종목수 적으면 전체 랭킹 사용
#         grp_size = df_top.groupby("Sector")["name"].transform("size")
#         small_grp = grp_size < 3
#         for c_pair in [("div_pct", "div_pct_all"), ("roe_pct", "roe_pct_all"), ("per_pct", "per_pct_all"), ("pbr_pct", "pbr_pct_all")]:
#             df_top.loc[small_grp, c_pair[0]] = df_top.loc[small_grp, c_pair[1]]
#     else:
#         df_top["div_pct"] = df_top["div_pct_all"]
#         df_top["roe_pct"] = df_top["roe_pct_all"]
#         df_top["per_pct"] = df_top["per_pct_all"]
#         df_top["pbr_pct"] = df_top["pbr_pct_all"]

#     # 9) 최종 점수 ✨ [핵심] 수신된 가중치로 계산
#     df_top["base_score"] = (
#         current_cfg["w_roe"] * df_top["roe_pct"] +
#         current_cfg["w_div"] * df_top["div_pct"] +
#         current_cfg["w_per"] * df_top["per_pct"] +
#         current_cfg["w_pbr"] * df_top["pbr_pct"]
#     )

#     df_top["score"] = df_top["base_score"]

#     # PER, PBR 이상치 제거
#     df_top = df_top[df_top["PER"] > 0]
#     df_top = df_top[df_top["PBR"] > 0]

#     # 티커 정리
#     df_top["ticker"] = df_top.index.astype(str).str.zfill(6)

#     ranked = df_top.sort_values("score", ascending=False).reset_index(drop=True)
#     ranked["score"] = ranked["score"].round(2)

#     TOP_N = int(current_cfg["report_top"])
#     disp_cols = ["ticker", "name", "score", "DIV", "ROE_est", "PER", "PBR", "Sector"]
#     disp_cols = [c for c in disp_cols if c in ranked.columns]

#     return BASE_DATE, ranked[disp_cols].head(TOP_N)


# # ================================
# # ✅ API 호출용 래퍼 함수 (views.py가 이걸 부름)
# # ================================
# def get_stock_ranking(limit: Optional[int] = None, weights: Optional[Dict[str, float]] = None) -> Dict[str, object]:
    
#     # 1. CFG 복사 및 가중치 덮어쓰기 ✨ [핵심]
#     current_cfg = CFG.copy()
#     if weights:
#         for k, v in weights.items():
#             if k in current_cfg:
#                 current_cfg[k] = v # w_div, w_roe 등의 값을 덮어씁니다.
    
#     try:
#         # 수정된 CFG를 가지고 분석 엔진 실행
#         base_date, df = calculate_ranking_logic(current_cfg)

#         if df is None or df.empty:
#             print("🚨 [Alert] 분석된 종목이 없습니다.")
#             return {"base_date": base_date, "rows": []}

#         if limit:
#             df = df.head(limit)

#         # JSON 변환을 위한 NaN 처리
#         df = df.replace([np.inf, -np.inf], np.nan)
#         df = df.fillna(0) 
        
#         rows = df.to_dict(orient="records")
        
#         print(f"✅ [Success] {len(rows)}개 종목 분석 및 변환 완료! (기준: {current_cfg['w_div']}/{current_cfg['w_roe']})")
        
#         return {
#             "base_date": base_date,
#             "rows": rows,
#         }

#     except Exception as e:
#         print(f"🔥 [Error] utils.py 실행 중 오류: {e}")
#         return {"base_date": datetime.today().strftime("%Y%m%d"), "rows": []}