from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Transportation
from .serializers import TransportationSerializer


class TransportationListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        include_inactive = request.query_params.get('include_inactive', 'false').lower() == 'true'
        queryset = Transportation.objects.select_related('type_transport').order_by('id')
        if not include_inactive:
            queryset = queryset.filter(active=True)

        serializer = TransportationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TransportationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos invalidos para crear el transporte.', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        transportation = serializer.save()
        output = TransportationSerializer(transportation)
        return Response(output.data, status=status.HTTP_201_CREATED)


class TransportationDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    non_editable_fields = {'active'}

    def get_object(self, transportation_id):
        try:
            return Transportation.objects.select_related('type_transport').get(pk=transportation_id)
        except Transportation.DoesNotExist:
            return None

    def get(self, request, transportation_id):
        transportation = self.get_object(transportation_id)
        if not transportation:
            return Response({'error': 'Transporte no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransportationSerializer(transportation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, transportation_id):
        return self._update(request, transportation_id, partial=False)

    def patch(self, request, transportation_id):
        return self._update(request, transportation_id, partial=True)

    def _update(self, request, transportation_id, partial):
        transportation = self.get_object(transportation_id)
        if not transportation:
            return Response({'error': 'Transporte no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        forbidden = self.non_editable_fields.intersection(set(request.data.keys()))
        if forbidden:
            return Response(
                {
                    'error': 'No se permite editar active.',
                    'fields': sorted(list(forbidden)),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TransportationSerializer(transportation, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos invalidos para actualizar el transporte.', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, transportation_id):
        transportation = self.get_object(transportation_id)
        if not transportation:
            return Response({'error': 'Transporte no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not transportation.active:
            return Response({'message': 'El transporte ya estaba inactivo.'}, status=status.HTTP_200_OK)

        transportation.active = False
        transportation.save(update_fields=['active'])
        return Response({'message': 'Transporte eliminado.'}, status=status.HTTP_200_OK)
