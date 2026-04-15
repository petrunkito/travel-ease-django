from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Client
from .serializers import ClientSerializer


class ClientListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        include_inactive = request.query_params.get('include_inactive', 'false').lower() == 'true'
        queryset = Client.objects.select_related('municipality', 'created_by').order_by('id')
        if not include_inactive:
            queryset = queryset.filter(active=True)

        serializer = ClientSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos invalidos para crear el cliente.', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        client = serializer.save(created_by=request.user)
        output = ClientSerializer(client)
        return Response(output.data, status=status.HTTP_201_CREATED)


class ClientDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    non_editable_fields = {'registration_date', 'active'}

    def get_object(self, client_id):
        try:
            return Client.objects.select_related('municipality', 'created_by').get(pk=client_id)
        except Client.DoesNotExist:
            return None

    def get(self, request, client_id):
        client = self.get_object(client_id)
        if not client:
            return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, client_id):
        return self._update(request, client_id, partial=False)

    def patch(self, request, client_id):
        return self._update(request, client_id, partial=True)

    def _update(self, request, client_id, partial):
        client = self.get_object(client_id)
        if not client:
            return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        forbidden = self.non_editable_fields.intersection(set(request.data.keys()))
        if forbidden:
            return Response(
                {
                    'error': 'No se permite editar registration_date ni active.',
                    'fields': sorted(list(forbidden)),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ClientSerializer(client, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos invalidos para actualizar el cliente.', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, client_id):
        client = self.get_object(client_id)
        if not client:
            return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not client.active:
            return Response(
                {'message': 'El cliente ya estaba inactivo.'},
                status=status.HTTP_200_OK,
            )

        client.active = False
        client.save(update_fields=['active'])
        return Response({'message': 'Cliente eliminado.'}, status=status.HTTP_200_OK)
