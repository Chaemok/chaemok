# backend/debug_pykrx.py
from pykrx import stock
import pandas as pd

print("============== [Pykrx 진단 시작] ==============")

# 1. 2025년 1월 10일 데이터 요청
target_date = "20250110"
print(f"1. {target_date} 데이터 요청 중...")

try:
    df = stock.get_market_fundamental_by_ticker(target_date, market="KOSPI")
    
    print("\n2. 데이터 수신 결과:")
    if df.empty:
        print("❌ 데이터프레임이 비어있습니다 (Empty DataFrame).")
    else:
        print(f"✅ 데이터 들어옴! (행 개수: {len(df)})")
        print(f"✅ 가지고 있는 컬럼 목록:\n{df.columns.tolist()}")
        print("\n✅ 데이터 샘플 (상위 2개):")
        print(df.head(2))

except Exception as e:
    print(f"❌ 치명적 에러 발생: {e}")

print("\n=============================================")