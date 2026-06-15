from rest_framework import serializers

from api.services.models import PriceHistory
from api.services.pricing import get_active_price, set_service_price

from .models import Transportation


class TransportationSerializer(serializers.ModelSerializer):
    type_transport_name = serializers.CharField(source='type_transport.name', read_only=True)
    type_transport_code = serializers.CharField(source='type_transport.code', read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True, required=False)
    current_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Transportation
        fields = [
            'id',
            'type_transport',
            'type_transport_name',
            'type_transport_code',
            'origin',
            'destination',
            'price',
            'current_price',
            'active',
        ]
        read_only_fields = ['id', 'active', 'current_price']

    def validate(self, attrs):
        if self.instance and 'price' in attrs:
            raise serializers.ValidationError(
                {'price': 'Para cambiar el precio usa el endpoint /api/services/transportation/{id}/prices/.'}
            )
        return attrs

    def create(self, validated_data):
        price = validated_data.pop('price', None)
        if price is None:
            raise serializers.ValidationError({'price': 'El precio es requerido para crear el transporte.'})

        transportation = super().create(validated_data)
        set_service_price(PriceHistory.ServiceType.TRANSPORTATION, transportation.id, price)
        return transportation

    def get_current_price(self, obj):
        price_row = get_active_price(PriceHistory.ServiceType.TRANSPORTATION, obj.id)
        return price_row.price if price_row else None
