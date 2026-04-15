from rest_framework import serializers

from .models import TypeTransport


class TypeTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeTransport
        fields = ['id', 'name', 'code', 'active']
        read_only_fields = ['id', 'active']
