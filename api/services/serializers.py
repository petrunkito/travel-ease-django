from decimal import Decimal

from rest_framework import serializers

from .models import PriceHistory


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['id', 'service_type', 'service_id', 'price', 'start_date', 'end_date']
        read_only_fields = fields


class ServicePriceUpdateSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
