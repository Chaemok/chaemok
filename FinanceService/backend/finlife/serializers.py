from rest_framework import serializers
from .models import DepositProduct, DepositOptions, SavingProduct, SavingOptions, ExchangeRate

# --- 1. 환율 ---
class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = '__all__'

# --- 2. 예금 관련 ---
class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('product',)

class DepositProductSerializer(serializers.ModelSerializer):
    intr_rate = serializers.SerializerMethodField()
    max_intr_rate = serializers.SerializerMethodField()
    options = DepositOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = DepositProduct
        fields = '__all__'

    def get_intr_rate(self, obj):
        # 🐜 related_name 설정과 상관없이 가장 안전하게 첫 번째 옵션을 가져오는 방법
        options = obj.depositoptions_set.all() if hasattr(obj, 'depositoptions_set') else obj.options.all()
        first_opt = options.first()
        return first_opt.intr_rate if first_opt else 0

    def get_max_intr_rate(self, obj):
        options = obj.depositoptions_set.all() if hasattr(obj, 'depositoptions_set') else obj.options.all()
        if options.exists():
            return max([opt.intr_rate2 for opt in options if opt.intr_rate2 is not None] or [0])
        return 0

# --- 3. 적금 관련 ---
class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('product',)

class SavingProductSerializer(serializers.ModelSerializer):
    intr_rate = serializers.SerializerMethodField()
    max_intr_rate = serializers.SerializerMethodField()
    options = SavingOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = SavingProduct
        fields = '__all__'

    def get_intr_rate(self, obj):
        options = obj.savingoptions_set.all() if hasattr(obj, 'savingoptions_set') else obj.options.all()
        first_opt = options.first()
        return first_opt.intr_rate if first_opt else 0

    def get_max_intr_rate(self, obj):
        options = obj.savingoptions_set.all() if hasattr(obj, 'savingoptions_set') else obj.options.all()
        if options.exists():
            return max([opt.intr_rate2 for opt in options if opt.intr_rate2 is not None] or [0])
        return 0

# --- 4. 기타 조회용 ---
class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = ('kor_co_nm', 'fin_prdt_nm')

class JoinedDepositOptionSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer(read_only=True)
    class Meta:
        model = DepositOptions
        fields = '__all__'