from rest_framework import generics

from .models import Municipality
from .serializers import MunicipalitySerializer


class MunicipalityListCreateAPIView(generics.ListCreateAPIView):
    queryset = Municipality.objects.select_related('department').all().order_by('id')
    serializer_class = MunicipalitySerializer
