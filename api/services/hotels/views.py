from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Hotel
from .serializers import HotelSerializer


class HotelListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        include_inactive = request.query_params.get('include_inactive', 'false').lower() == 'true'
        queryset = Hotel.objects.order_by('id')
        if not include_inactive:
            queryset = queryset.filter(active=True)

        serializer = HotelSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HotelSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos invalidos para crear el hotel.', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        hotel = serializer.save()
        output = HotelSerializer(hotel)
        return Response(output.data, status=status.HTTP_201_CREATED)


class HotelDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    non_editable_fields = {'active'}

    def get_object(self, hotel_id):
        try:
            return Hotel.objects.get(pk=hotel_id)
        except Hotel.DoesNotExist:
            return None

    def get(self, request, hotel_id):
        hotel = self.get_object(hotel_id)
        if not hotel:
            return Response({'error': 'Hotel no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = HotelSerializer(hotel)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, hotel_id):
        return self._update(request, hotel_id, partial=False)

    def patch(self, request, hotel_id):
        return self._update(request, hotel_id, partial=True)

    def _update(self, request, hotel_id, partial):
        hotel = self.get_object(hotel_id)
        if not hotel:
            return Response({'error': 'Hotel no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        forbidden = self.non_editable_fields.intersection(set(request.data.keys()))
        if forbidden:
            return Response(
                {
                    'error': 'No se permite editar active.',
                    'fields': sorted(list(forbidden)),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = HotelSerializer(hotel, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos invalidos para actualizar el hotel.', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, hotel_id):
        hotel = self.get_object(hotel_id)
        if not hotel:
            return Response({'error': 'Hotel no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not hotel.active:
            return Response({'message': 'El hotel ya estaba inactivo.'}, status=status.HTTP_200_OK)

        hotel.active = False
        hotel.save(update_fields=['active'])
        return Response({'message': 'Hotel eliminado.'}, status=status.HTTP_200_OK)
