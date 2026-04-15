from rest_framework import serializers

from .models import Transportation


class TransportationSerializer(serializers.ModelSerializer):
    type_transport_name = serializers.CharField(source='type_transport.name', read_only=True)
    type_transport_code = serializers.CharField(source='type_transport.code', read_only=True)

    class Meta:
        model = Transportation
        fields = [
            'id',
            'type_transport',
            'type_transport_name',
            'type_transport_code',
            'origin',
            'destination',
            'active',
        ]
        read_only_fields = ['id', 'active']
