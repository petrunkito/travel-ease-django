from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Reservation, ReservationDetail, ReservationStatus,
    ReservationStatusHistory, PaymentType, Invoice
)
from .serializers import (
    ReservationCreateSerializer, ReservationDetailedSerializer,
    ReservationUpdateStatusSerializer, ReservationDetailSerializer,
    ReservationStatusHistorySerializer, PaymentTypeSerializer,
    ReservationStatusSerializer, InvoiceSerializer
)


class PaymentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para listar tipos de pago."""
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer


class ReservationStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para listar estados de reserva."""
    queryset = ReservationStatus.objects.all()
    serializer_class = ReservationStatusSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar reservas.
    
    Operaciones disponibles:
    - GET /reservations/ - Listar todas las reservas
    - GET /reservations/{id}/ - Obtener detalle de una reserva
    - POST /reservations/ - Crear una nueva reserva (genera factura automáticamente)
    - PUT /reservations/{id}/ - Actualizar una reserva
    - DELETE /reservations/{id}/ - Eliminar (desactivar) una reserva
    - PUT /reservations/{id}/update_status/ - Cambiar estado de una reserva
    - GET /reservations/{id}/status_history/ - Ver historial de cambios de estado
    """
    queryset = Reservation.objects.filter(active=True)
    serializer_class = ReservationDetailedSerializer

    def get_serializer_class(self):
        """Retorna el serializer adecuado según la acción."""
        if self.action == 'create':
            return ReservationCreateSerializer
        elif self.action == 'update_status':
            return ReservationUpdateStatusSerializer
        return ReservationDetailedSerializer

    def create(self, request, *args, **kwargs):
        """Crear una nueva reserva."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save()
        
        output_serializer = ReservationDetailedSerializer(reservation)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        """
        Actualizar el estado de una reserva.
        
        No permite cambiar el estado si la reserva está en estado Pagado o Cancelado.
        """
        reservation = self.get_object()

        # Verificar si la reserva está en estado final
        current_status = reservation.status_history.order_by('-date').first()
        if current_status and current_status.status.code in ['PAG', 'CANC']:
            return Response(
                {
                    'error': 'No se puede cambiar el estado de una reserva en estado Pagado o Cancelado.',
                    'current_status': current_status.status.code
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        status_id = serializer.validated_data['status_id']
        new_status = ReservationStatus.objects.get(id=status_id)

        # Crear nuevo registro en el historial de estados
        ReservationStatusHistory.objects.create(
            reservation=reservation,
            status=new_status
        )

        output_serializer = ReservationDetailedSerializer(reservation)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Desactivar una reserva (soft delete)."""
        reservation = self.get_object()
        reservation.active = False
        reservation.save()
        return Response(
            {'message': 'Reserva desactivada correctamente.'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=['get'])
    def status_history(self, request, pk=None):
        """Obtener el historial de cambios de estado de una reserva."""
        reservation = self.get_object()
        history = reservation.status_history.all().order_by('-date')
        serializer = ReservationStatusHistorySerializer(history, many=True)
        return Response(serializer.data)

