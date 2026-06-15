from rest_framework import serializers

from api.services.models import PriceHistory
from api.services.pricing import get_active_price, set_service_price

from .models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True, required=False)
    current_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'city', 'stars', 'category', 'price', 'current_price', 'active']
        read_only_fields = ['id', 'active', 'current_price']

    def validate_stars(self, value):
        if value is None:
            return value

        if value < 1 or value > 5:
            raise serializers.ValidationError('La cantidad de estrellas debe estar entre 1 y 5.')
        return value

    def validate(self, attrs):
        if self.instance and 'price' in attrs:
            raise serializers.ValidationError(
                {'price': 'Para cambiar el precio usa el endpoint /api/services/hotels/{id}/prices/.'}
            )
        return attrs

    def create(self, validated_data):
        price = validated_data.pop('price', None)
        if price is None:
            raise serializers.ValidationError({'price': 'El precio es requerido para crear el hotel.'})

        hotel = super().create(validated_data)
        set_service_price(PriceHistory.ServiceType.HOTEL, hotel.id, price)
        return hotel

    def get_current_price(self, obj):
        price_row = get_active_price(PriceHistory.ServiceType.HOTEL, obj.id)
        return price_row.price if price_row else None
