from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TypeTransport
from .serializers import TypeTransportSerializer


class TypeTransportListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        include_inactive = request.query_params.get('include_inactive', 'false').lower() == 'true'
        queryset = TypeTransport.objects.order_by('id')
        if not include_inactive:
            queryset = queryset.filter(active=True)

        serializer = TypeTransportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TypeTransportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos invalidos para crear el tipo de transporte.', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        type_transport = serializer.save()
        output = TypeTransportSerializer(type_transport)
        return Response(output.data, status=status.HTTP_201_CREATED)


class TypeTransportDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    non_editable_fields = {'active'}

    def get_object(self, type_transport_id):
        try:
            return TypeTransport.objects.get(pk=type_transport_id)
        except TypeTransport.DoesNotExist:
            return None

    def get(self, request, type_transport_id):
        type_transport = self.get_object(type_transport_id)
        if not type_transport:
            return Response({'error': 'Tipo de transporte no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TypeTransportSerializer(type_transport)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, type_transport_id):
        return self._update(request, type_transport_id, partial=False)

    def patch(self, request, type_transport_id):
        return self._update(request, type_transport_id, partial=True)

    def _update(self, request, type_transport_id, partial):
        type_transport = self.get_object(type_transport_id)
        if not type_transport:
            return Response({'error': 'Tipo de transporte no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        forbidden = self.non_editable_fields.intersection(set(request.data.keys()))
        if forbidden:
            return Response(
                {
                    'error': 'No se permite editar active.',
                    'fields': sorted(list(forbidden)),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TypeTransportSerializer(type_transport, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos invalidos para actualizar el tipo de transporte.', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, type_transport_id):
        type_transport = self.get_object(type_transport_id)
        if not type_transport:
            return Response({'error': 'Tipo de transporte no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not type_transport.active:
            return Response({'message': 'El tipo de transporte ya estaba inactivo.'}, status=status.HTTP_200_OK)

        type_transport.active = False
        type_transport.save(update_fields=['active'])
        return Response({'message': 'Tipo de transporte eliminado.'}, status=status.HTTP_200_OK)
