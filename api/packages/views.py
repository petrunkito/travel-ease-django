from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TouristPackage
from .serializers import TouristPackageSerializer


class TouristPackageListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        include_inactive = request.query_params.get('include_inactive', 'false').lower() == 'true'
        queryset = TouristPackage.objects.select_related('destination', 'created_by').prefetch_related('details').order_by('id')
        if not include_inactive:
            queryset = queryset.filter(active=True)

        serializer = TouristPackageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TouristPackageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos invalidos para crear el paquete turistico.', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tourist_package = serializer.save(created_by=request.user)
        output = TouristPackageSerializer(tourist_package)
        return Response(output.data, status=status.HTTP_201_CREATED)


class TouristPackageDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    non_editable_fields = {'active', 'created_at'}

    def get_object(self, package_id):
        try:
            return TouristPackage.objects.select_related('destination', 'created_by').prefetch_related('details').get(pk=package_id)
        except TouristPackage.DoesNotExist:
            return None

    def get(self, request, package_id):
        tourist_package = self.get_object(package_id)
        if not tourist_package:
            return Response({'error': 'Paquete turistico no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TouristPackageSerializer(tourist_package)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, package_id):
        return self._update(request, package_id, partial=False)

    def patch(self, request, package_id):
        return self._update(request, package_id, partial=True)

    def _update(self, request, package_id, partial):
        tourist_package = self.get_object(package_id)
        if not tourist_package:
            return Response({'error': 'Paquete turistico no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        forbidden = self.non_editable_fields.intersection(set(request.data.keys()))
        if forbidden:
            return Response(
                {
                    'error': 'No se permite editar active ni created_at.',
                    'fields': sorted(list(forbidden)),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TouristPackageSerializer(tourist_package, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos invalidos para actualizar el paquete turistico.', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, package_id):
        tourist_package = self.get_object(package_id)
        if not tourist_package:
            return Response({'error': 'Paquete turistico no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not tourist_package.active:
            return Response({'message': 'El paquete turistico ya estaba inactivo.'}, status=status.HTTP_200_OK)

        tourist_package.active = False
        tourist_package.save(update_fields=['active'])
        return Response({'message': 'Paquete turistico eliminado.'}, status=status.HTTP_200_OK)
