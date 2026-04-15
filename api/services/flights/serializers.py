from rest_framework import serializers

from .models import Flight


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = [
            'id',
            'airline',
            'origin',
            'destination',
            'departure_date',
            'arrival_date',
            'active',
        ]
        read_only_fields = ['id', 'active']

    def validate(self, attrs):
        departure_date = attrs.get('departure_date', getattr(self.instance, 'departure_date', None))
        arrival_date = attrs.get('arrival_date', getattr(self.instance, 'arrival_date', None))

        if departure_date and arrival_date and arrival_date <= departure_date:
            raise serializers.ValidationError(
                {'arrival_date': 'La fecha de llegada debe ser mayor que la fecha de salida.'}
            )

        return attrs
