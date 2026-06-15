from rest_framework import serializers

from api.services.models import PriceHistory
from api.services.pricing import get_active_price, set_service_price

from .models import Flight


class FlightSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True, required=False)
    current_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Flight
        fields = [
            'id',
            'airline',
            'origin',
            'destination',
            'departure_date',
            'arrival_date',
            'price',
            'current_price',
            'active',
        ]
        read_only_fields = ['id', 'active', 'current_price']

    def validate(self, attrs):
        departure_date = attrs.get('departure_date', getattr(self.instance, 'departure_date', None))
        arrival_date = attrs.get('arrival_date', getattr(self.instance, 'arrival_date', None))

        if departure_date and arrival_date and arrival_date <= departure_date:
            raise serializers.ValidationError(
                {'arrival_date': 'La fecha de llegada debe ser mayor que la fecha de salida.'}
            )

        if self.instance and 'price' in attrs:
            raise serializers.ValidationError(
                {'price': 'Para cambiar el precio usa el endpoint /api/services/flights/{id}/prices/.'}
            )

        return attrs

    def create(self, validated_data):
        price = validated_data.pop('price', None)
        if price is None:
            raise serializers.ValidationError({'price': 'El precio es requerido para crear el vuelo.'})

        flight = super().create(validated_data)
        set_service_price(PriceHistory.ServiceType.FLIGHT, flight.id, price)
        return flight

    def get_current_price(self, obj):
        price_row = get_active_price(PriceHistory.ServiceType.FLIGHT, obj.id)
        return price_row.price if price_row else None
