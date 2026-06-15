from rest_framework import serializers

from .models import Municipality


class MunicipalitySerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)

    class Meta:
        model = Municipality
        fields = ['id', 'department', 'department_name', 'department_code', 'name', 'code']
