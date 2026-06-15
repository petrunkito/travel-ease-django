from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.catalogos.departamentos.models import Department

from .models import Municipality
from .serializers import MunicipalitySerializer


class MunicipalityListCreateAPIView(generics.ListCreateAPIView):
    queryset = Municipality.objects.select_related('department').all().order_by('id')
    serializer_class = MunicipalitySerializer


class MunicipalityByDepartmentAPIView(APIView):
    def get(self, request, department_id):
        department_exists = Department.objects.filter(pk=department_id).exists()
        if not department_exists:
            return Response({'error': 'Departamento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        queryset = (
            Municipality.objects.select_related('department')
            .filter(department_id=department_id)
            .order_by('id')
        )
        serializer = MunicipalitySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
