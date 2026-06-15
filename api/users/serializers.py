from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model()


class EmployeeCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=['ADMIN', 'ASISTENTE'], required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        role_name = validated_data.pop('role', 'ASISTENTE')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.is_staff = True
        user.save()

        group = Group.objects.get(name=role_name)
        user.groups.add(group)
        return user


class EmployeeListSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'roles',
        ]

    def get_roles(self, obj):
        return list(obj.groups.values_list('name', flat=True))
