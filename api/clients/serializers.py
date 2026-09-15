from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Client

User = get_user_model()


class ClientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=False)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    municipality_name = serializers.CharField(source='municipality.name', read_only=True)
    municipality_code = serializers.CharField(source='municipality.code', read_only=True)
    department_id = serializers.IntegerField(source='municipality.department.id', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Client
        fields = [
            'id',
            'user_id',
            'user_email',
            'email',
            'municipality',
            'municipality_name',
            'municipality_code',
            'department_id',
            'created_by',
            'created_by_username',
            'name',
            'national_id',
            'address',
            'phone_number',
            'registration_date',
            'active',
        ]
        read_only_fields = ['id', 'user', 'user_id', 'user_email', 'created_by', 'registration_date', 'active']

    def validate_email(self, value):
        if self.instance is None and User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError('El correo ya esta registrado.')
        if self.instance is not None:
            raise serializers.ValidationError('El correo no se puede editar.')
        return value

    def validate(self, attrs):
        if self.instance is None and not attrs.get('email'):
            raise serializers.ValidationError({'email': 'El correo es obligatorio para crear el cliente.'})
        return attrs
