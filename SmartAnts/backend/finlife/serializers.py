from rest_framework import serializers
from .models import DepositProduct, DepositOptions, SavingProduct, SavingOptions, ExchangeRate

# --- 1. 환율 ---
class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = '__all__'

# ==========================================================
# 🐜 [순환 참조 방지용] 단순 상품 정보 시리얼라이저
# (옵션 정보 없이 상품 이름, 은행명 등만 가져옴)
# ==========================================================
class SimpleDepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'

class SimpleSavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'


# ==========================================================
# 2. 옵션 시리얼라이저 (상품 정보 포함)
# ==========================================================
class DepositOptionsSerializer(serializers.ModelSerializer):
    # 부모 상품 정보(이름, 은행 등)를 포함
    product = SimpleDepositProductSerializer(read_only=True)

    class Meta:
        model = DepositOptions
        fields = '__all__'

class SavingOptionsSerializer(serializers.ModelSerializer):
    # 부모 상품 정보(이름, 은행 등)를 포함
    product = SimpleSavingProductSerializer(read_only=True)

    class Meta:
        model = SavingOptions
        fields = '__all__'


# ==========================================================
# 3. 상품 상세 시리얼라이저 (옵션 리스트 포함)
# ==========================================================
class DepositProductSerializer(serializers.ModelSerializer):
    # Simple 버전을 쓰지 않고, 위에서 정의한 OptionsSerializer 사용
    options = DepositOptionsSerializer(many=True, read_only=True)
    intr_rate = serializers.SerializerMethodField()
    max_intr_rate = serializers.SerializerMethodField()

    class Meta:
        model = DepositProduct
        fields = '__all__'

    def get_intr_rate(self, obj):
        # 역참조 매니저 이름 확인 (depositoptions_set 또는 options)
        options = getattr(obj, 'depositoptions_set', getattr(obj, 'options', None))
        return options.first().intr_rate if (options and options.exists()) else 0

    def get_max_intr_rate(self, obj):
        options = getattr(obj, 'depositoptions_set', getattr(obj, 'options', None))
        if options and options.exists():
            rates = [opt.intr_rate2 for opt in options.all() if opt.intr_rate2 is not None]
            return max(rates) if rates else 0
        return 0

class SavingProductSerializer(serializers.ModelSerializer):
    options = SavingOptionsSerializer(many=True, read_only=True)
    intr_rate = serializers.SerializerMethodField()
    max_intr_rate = serializers.SerializerMethodField()

    class Meta:
        model = SavingProduct
        fields = '__all__'

    def get_intr_rate(self, obj):
        options = getattr(obj, 'savingoptions_set', getattr(obj, 'options', None))
        return options.first().intr_rate if (options and options.exists()) else 0

    def get_max_intr_rate(self, obj):
        options = getattr(obj, 'savingoptions_set', getattr(obj, 'options', None))
        if options and options.exists():
            rates = [opt.intr_rate2 for opt in options.all() if opt.intr_rate2 is not None]
            return max(rates) if rates else 0
        return 0


# ==========================================================
# 4. 가입 상품용 시리얼라이저 (Joined...)
# ==========================================================
class JoinedDepositOptionSerializer(serializers.ModelSerializer):
    product = SimpleDepositProductSerializer(read_only=True)
    
    class Meta:
        model = DepositOptions
        fields = '__all__'

class JoinedSavingOptionSerializer(serializers.ModelSerializer):
    product = SimpleSavingProductSerializer(read_only=True)
    
    class Meta:
        model = SavingOptions
        fields = '__all__'