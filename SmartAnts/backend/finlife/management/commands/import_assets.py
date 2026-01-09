# backend/finlife/management/commands/import_assets.py
import pandas as pd
from django.core.management.base import BaseCommand
from finlife.models import AssetPrice
from datetime import datetime

class Command(BaseCommand):
    help = 'Import gold and silver prices from Excel files'

    def handle(self, *args, **options):
        assets = [
            {'file': 'backend/data/Gold_prices.xlsx', 'type': 'gold'},
            {'file': 'backend/data/Silver_prices.xlsx', 'type': 'silver'}
        ]

        for asset in assets:
            try:
                # 엑셀 파일 읽기 (Date, Price 컬럼이 있다고 가정)
                df = pd.read_excel(asset['file'])
                
                count = 0
                for _, row in df.iterrows():
                    # 날짜와 가격 추출 (파일 형식에 따라 컬럼명 수정 필요)
                    date_val = row['Date']
                    if isinstance(date_val, str):
                        date_val = datetime.strptime(date_val, '%Y-%m-%d').date()
                    
                    # 중복 방지를 위해 update_or_create 사용
                    AssetPrice.objects.update_or_create(
                        asset_type=asset['type'],
                        date=date_val,
                        defaults={'price': row['Price']}
                    )
                    count += 1
                
                self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} {asset['type']} records"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error importing {asset['type']}: {e}"))