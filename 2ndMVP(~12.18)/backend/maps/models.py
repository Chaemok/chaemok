from django.db import models


class Place(models.Model):
    """
    지도에 표시할 장소 (은행, 증권사, ATM 등)
    """

    CATEGORY_CHOICES = [
        ('BANK', '은행'),
        ('SECURITIES', '증권사'),
        ('ATM', 'ATM'),
        ('OTHER', '기타'),
    ]

    name = models.CharField(max_length=200)          # 지점/점포 이름
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='BANK',
    )
    address = models.CharField(max_length=300, blank=True)

    lat = models.FloatField()    # 위도
    lng = models.FloatField()    # 경도

    # 예: 국민은행, 신한은행, 미래에셋 같은 상호
    org_name = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.name}"