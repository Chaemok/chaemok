import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from pykrx import stock

# FinanceDataReader는 업종 정보용(없어도 동작)
try:
    import FinanceDataReader as fdr
    HAS_FDR = True
except Exception:
    HAS_FDR = False


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


def get_latest_bday(max_lookback_days=10, market="KOSPI"):
    """가장 최근 영업일 문자열(YYYYMMDD) 찾기"""
    today = datetime.today().date()
    for i in range(max_lookback_days):
        d = (today - timedelta(days=i)).strftime("%Y%m%d")
        try:
            df = stock.get_market_fundamental_by_ticker(d, market=market)
            if isinstance(df, pd.DataFrame) and len(df) > 0:
                return d
        except Exception:
            pass
    raise RuntimeError("기준일 탐색 실패")


def safe_sector_dataframe():
    """FDR에서 섹터 정보 가져오기 (없으면 None)"""
    if not HAS_FDR:
        return None
    try:
        krx_list = fdr.StockListing("KRX")
        # 컬럼 이름 정리
        rename_map = {
            "Symbol": "ticker",
            "Name": "fdr_name",
        }
        for k, v in rename_map.items():
            if k in krx_list.columns:
                krx_list = krx_list.rename(columns={k: v})

        krx_list["ticker"] = krx_list["ticker"].astype(str).str.zfill(6)

        for col in ["Sector", "Industry", "Market"]:
            if col not in krx_list.columns:
                krx_list[col] = np.nan

        return krx_list.set_index("ticker")[["fdr_name", "Sector", "Industry", "Market"]]
    except Exception:
        return None


def choose_sector(row):
    """Sector / Industry / Market 중 하나로 섹터 결정"""
    for col in ["Sector", "Industry", "Market"]:
        val = row.get(col, None)
        if isinstance(val, str) and val:
            return val
    return "기타"


def pct_rank(s: pd.Series, higher=True) -> pd.Series:
    """
    시리즈를 0~100 백분위 점수로 변환
    higher=True : 값이 클수록 좋은 점수
    higher=False: 값이 낮을수록 좋은 점수
    """
    s = s.fillna(0)
    rank = s.rank(pct=True, ascending=not higher) * 100
    return rank.clip(upper=99.99)


def get_dividend_ranking():
    """
    추천 API에서 호출할 핵심 함수
    return: (base_date, df)
      - base_date: 기준일(문자열)
      - df: 상위 N개 랭킹 DataFrame
            컬럼: ticker, name, score, DIV, ROE_est, PER, PBR, Sector
    """
    BASE_DATE = get_latest_bday(market=CFG["market"])

    # 1) 기본 재무 지표
    fund = stock.get_market_fundamental_by_ticker(BASE_DATE, market=CFG["market"]).copy()
    need_cols = ["PER", "PBR", "EPS", "BPS", "DPS", "DIV"]
    for col in need_cols:
        if col not in fund.columns:
            fund[col] = np.nan
    fund = fund.replace([np.inf, -np.inf], np.nan)
    fund["DPS"] = fund["DPS"].fillna(0)
    fund["EPS"] = fund["EPS"].fillna(0)

    # 2) 시총/거래대금
    cap = stock.get_market_cap_by_ticker(BASE_DATE, market=CFG["market"]).copy()
    if "거래대금" not in cap.columns:
        cap["거래대금"] = np.nan
    if "상장주식수" in cap.columns:
        df = fund.join(cap[["거래대금", "상장주식수"]], how="left")
    else:
        df = fund.join(cap[["거래대금"]], how="left")

    # 3) 종목명/섹터
    tickers = df.index.tolist()
    name_map = {t: stock.get_market_ticker_name(t) for t in tickers}
    df["name"] = df.index.map(name_map.get)

    meta = safe_sector_dataframe()
    if meta is not None:
        df = df.join(meta, how="left")
    else:
        for col in ["fdr_name", "Sector", "Industry", "Market"]:
            if col not in df.columns:
                df[col] = np.nan
    df["Sector"] = df.apply(choose_sector, axis=1)

    # 4) 필터링 (우선주/스팩/리츠/금융/유동성)
    if CFG["exclude_pref_spac"]:
        name_series = df["name"].fillna("")
        df = df[~name_series.str.endswith("우")]
        df = df[~name_series.str.contains("우선|스팩|SPAC")]

    if not CFG["include_reits"]:
        df = df[~df.apply(lambda r: "리츠" in (r["name"] or "") or "REIT" in (r["Sector"] or ""), axis=1)]

    if not CFG["include_financials"]:
        df = df[~df["Sector"].fillna("").apply(lambda x: any(k in x for k in ["은행", "증권", "보험", "지주", "금융"]))]

    df = df[df["거래대금"].fillna(0) >= CFG["min_trading_value_krw"]].copy()

    # 5) ROE 근사
    df["ROE_est"] = np.where((df["BPS"] > 0) & df["EPS"].notna(), df["EPS"] / df["BPS"], np.nan)

    # 6) 배당 상위 N개만
    df_top = df.sort_values("DIV", ascending=False).head(CFG["top_n_div"]).copy()
    df_top["fcf_coverage"] = np.nan  # 자리만 잡아둠

    # 7) 백분위 점수
    df_top["div_pct_all"] = pct_rank(df_top["DIV"], True)      # 배당 높을수록 좋음
    df_top["roe_pct_all"] = pct_rank(df_top["ROE_est"], True)  # ROE 높을수록 좋음
    df_top["per_pct_all"] = pct_rank(df_top["PER"], False)     # PER 낮을수록 좋음
    df_top["pbr_pct_all"] = pct_rank(df_top["PBR"], False)     # PBR 낮을수록 좋음

    if CFG["apply_sector_adjust"]:
        def grp_pct(col, higher=True):
            return df_top.groupby("Sector")[col].transform(
                lambda s: s.rank(pct=True, ascending=not higher) * 100
            )

        df_top["div_pct"] = grp_pct("DIV", True)
        df_top["roe_pct"] = grp_pct("ROE_est", True)
        df_top["per_pct"] = grp_pct("PER", False)
        df_top["pbr_pct"] = grp_pct("PBR", False)

        grp_size = df_top.groupby("Sector")["name"].transform("size")
        small_grp = grp_size < 3
        for c_pair in [("div_pct", "div_pct_all"),
                       ("roe_pct", "roe_pct_all"),
                       ("per_pct", "per_pct_all"),
                       ("pbr_pct", "pbr_pct_all")]:
            df_top.loc[small_grp, c_pair[0]] = df_top.loc[small_grp, c_pair[1]]
    else:
        df_top["div_pct"] = df_top["div_pct_all"]
        df_top["roe_pct"] = df_top["roe_pct_all"]
        df_top["per_pct"] = df_top["per_pct_all"]
        df_top["pbr_pct"] = df_top["pbr_pct_all"]

    # 8) 최종 점수 계산
    df_top["base_score"] = (
        CFG["w_roe"] * df_top["roe_pct"] +
        CFG["w_div"] * df_top["div_pct"] +
        CFG["w_per"] * df_top["per_pct"] +
        CFG["w_pbr"] * df_top["pbr_pct"]
    )
    df_top["score"] = df_top["base_score"]

    # PER, PBR 0 이하 제거
    df_top = df_top[df_top["PER"] > 0]
    df_top = df_top[df_top["PBR"] > 0]

    # 티커 컬럼 보정
    df_top["ticker"] = df_top.index.astype(str).str.zfill(6)

    ranked = df_top.sort_values("score", ascending=False).reset_index(drop=True)
    ranked["score"] = ranked["score"].round(2)

    TOP_N = int(CFG["report_top"])
    disp_cols = ["ticker", "name", "score", "DIV", "ROE_est", "PER", "PBR", "Sector"]
    disp_cols = [c for c in disp_cols if c in ranked.columns]

    return BASE_DATE, ranked[disp_cols].head(TOP_N)
