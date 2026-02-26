# backend/finances/serializers.py
from rest_framework import serializers
from .models import DepositProduct, SavingProduct, ExchangeRate


class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'
        # 혹은 fields = ['id', 'bank_name', 'product_name', 'interest_rate', 'highest_rate', 'join_term']

class SavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'

class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = '__all__'