from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True,
    )

    class Meta:
        model = Place
        fields = [
            'id',
            'name',
            'org_name',
            'category',
            'category_display',
            'address',
            'lat',
            'lng',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']