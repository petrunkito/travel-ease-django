from rest_framework import serializers

from .models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'city', 'stars', 'category', 'active']
        read_only_fields = ['id', 'active']

    def validate_stars(self, value):
        if value is None:
            return value

        if value < 1 or value > 5:
            raise serializers.ValidationError('La cantidad de estrellas debe estar entre 1 y 5.')
        return value
