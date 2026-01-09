import requests
from bs4 import BeautifulSoup
import json
import os
import time

# =========================================================
# 🐜 네이버 업종명 -> GICS 11개 섹터 변환 맵
# =========================================================
def map_naver_to_gics(naver_sector):
    s = naver_sector.replace(" ", "")
    
    # 1. IT
    if any(k in s for k in ["반도체", "IT", "소프트웨어", "전자", "디스플레이", "컴퓨터", "통신장비", "핸드셋", "전자제품"]):
        return "IT"
    # 2. 헬스케어
    if any(k in s for k in ["제약", "바이오", "생명", "헬스", "건강", "의료"]):
        return "헬스케어"
    # 3. 금융
    if any(k in s for k in ["은행", "증권", "보험", "금융", "캐피탈", "투자", "지주"]):
        return "금융" # 지주사는 보통 금융으로 분류하거나 복합기업
    # 4. 커뮤니케이션
    if any(k in s for k in ["통신", "미디어", "엔터", "게임", "광고", "방송", "출판", "영화", "인터넷", "SNS"]):
        return "커뮤니케이션"
    # 5. 산업재 (가장 많음)
    if any(k in s for k in ["건설", "조선", "기계", "운송", "해운", "항공", "방산", "상사", "물류", "전선", "건축", "엔지니어링", "전기장비", "무역"]):
        return "산업재"
    # 6. 소재
    if any(k in s for k in ["화학", "철강", "금속", "비철", "시멘트", "제지", "비료", "유리", "광물", "포장", "섬유"]):
        return "소재"
    # 7. 필수소비재
    if any(k in s for k in ["음식료", "식품", "담배", "생활용품", "화장품", "음료"]):
        return "필수소비재"
    # 8. 경기소비재
    if any(k in s for k in ["자동차", "부품", "유통", "백화점", "의류", "호텔", "레저", "교육", "가구", "가전", "소매", "면세", "레저"]):
        return "경기소비재"
    # 9. 에너지
    if any(k in s for k in ["에너지", "정유", "석유", "가스", "LPG"]):
        return "에너지"
    # 10. 유틸리티
    if any(k in s for k in ["전력", "가스유틸", "수도", "환경", "폐기물"]):
        return "유틸리티"
    # 11. 부동산
    if any(k in s for k in ["부동산", "리츠"]):
        return "부동산"

    return "기타" # 여기에 걸리면 진짜 기타

def crawl_naver_sectors():
    print("🐜 네이버 금융 업종 데이터를 크롤링합니다... (약 10~20초 소요)")
    
    base_url = "https://finance.naver.com/sise/sise_group.naver?type=upjong"
    response = requests.get(base_url)
    
    # 인코딩 설정 (한글 깨짐 방지)
    response.encoding = 'euc-kr' 
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 업종 링크 찾기
    table = soup.find('table', {'class': 'type_1'})
    links = table.find_all('a')
    
    sector_map = {}
    
    print(f"   📊 총 {len(links)}개 세부 업종을 발견했습니다. 스캔 시작!")
    
    for i, link in enumerate(links):
        sector_name = link.text.strip()
        sector_url = "https://finance.naver.com" + link['href']
        
        # GICS로 변환
        gics_sector = map_naver_to_gics(sector_name)
        
        # 해당 업종 페이지 접속해서 종목 코드 긁어오기
        try:
            sub_res = requests.get(sector_url)
            sub_res.encoding = 'euc-kr'
            sub_soup = BeautifulSoup(sub_res.text, 'html.parser')
            
            # 종목 리스트 테이블
            sub_table = sub_soup.find('table', {'class': 'type_5'})
            stocks = sub_table.find_all('a')
            
            count = 0
            for stock in stocks:
                href = stock['href']
                if 'code=' in href:
                    code = href.split('code=')[1]
                    sector_map[code] = gics_sector
                    count += 1
            
            # 진행상황 출력 (너무 빠르면 네이버가 차단할 수 있으니 살짝 딜레이 줄 수도 있음)
            # print(f"   [{i+1}/{len(links)}] {sector_name} -> {gics_sector} ({count}개)")
            
        except Exception as e:
            print(f"   ❌ {sector_name} 크롤링 실패: {e}")
            continue

    # 파일 저장
    file_name = "sectors.json"
    current_path = os.getcwd()
    save_path = os.path.join(current_path, file_name)
    
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(sector_map, f, ensure_ascii=False, indent=2)
        
    print("\n✅ [완료] sectors.json 생성 성공!")
    print(f"   📂 저장 위치: {save_path}")
    print(f"   📊 매핑된 종목 수: {len(sector_map)}개")
    print("   📢 이 파일을 'backend/finlife/utils/' 폴더로 이동시켜주세요!")

if __name__ == "__main__":
    crawl_naver_sectors()