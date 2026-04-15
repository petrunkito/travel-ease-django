from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Flight
from .serializers import FlightSerializer


class FlightListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        include_inactive = request.query_params.get('include_inactive', 'false').lower() == 'true'
        queryset = Flight.objects.order_by('id')
        if not include_inactive:
            queryset = queryset.filter(active=True)

        serializer = FlightSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FlightSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos invalidos para crear el vuelo.', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        flight = serializer.save()
        output = FlightSerializer(flight)
        return Response(output.data, status=status.HTTP_201_CREATED)


class FlightDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    non_editable_fields = {'active'}

    def get_object(self, flight_id):
        try:
            return Flight.objects.get(pk=flight_id)
        except Flight.DoesNotExist:
            return None

    def get(self, request, flight_id):
        flight = self.get_object(flight_id)
        if not flight:
            return Response({'error': 'Vuelo no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FlightSerializer(flight)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, flight_id):
        return self._update(request, flight_id, partial=False)

    def patch(self, request, flight_id):
        return self._update(request, flight_id, partial=True)

    def _update(self, request, flight_id, partial):
        flight = self.get_object(flight_id)
        if not flight:
            return Response({'error': 'Vuelo no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        forbidden = self.non_editable_fields.intersection(set(request.data.keys()))
        if forbidden:
            return Response(
                {
                    'error': 'No se permite editar active.',
                    'fields': sorted(list(forbidden)),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = FlightSerializer(flight, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos invalidos para actualizar el vuelo.', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, flight_id):
        flight = self.get_object(flight_id)
        if not flight:
            return Response({'error': 'Vuelo no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not flight.active:
            return Response({'message': 'El vuelo ya estaba inactivo.'}, status=status.HTTP_200_OK)

        flight.active = False
        flight.save(update_fields=['active'])
        return Response({'message': 'Vuelo eliminado.'}, status=status.HTTP_200_OK)
