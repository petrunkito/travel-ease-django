from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    municipality_name = serializers.CharField(source='municipality.name', read_only=True)
    municipality_code = serializers.CharField(source='municipality.code', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Client
        fields = [
            'id',
            'municipality',
            'municipality_name',
            'municipality_code',
            'created_by',
            'created_by_username',
            'name',
            'national_id',
            'address',
            'phone_number',
            'registration_date',
            'active',
        ]
        read_only_fields = ['id', 'created_by', 'registration_date', 'active']
