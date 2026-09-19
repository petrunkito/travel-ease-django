from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery

from api.packages.models import TouristPackage
from api.reservations.models import ReservationDetail

class ClienteBaseAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        # Ejecuta la validación estándar de DRF
        super().initial(request, *args, **kwargs)

        # 1. Validar grupo "Cliente"
        if not request.user.groups.filter(name='Cliente').exists():
            raise PermissionDenied('Acceso denegado: No pertenece al grupo Cliente.')

        # 2. Adjuntar los datos del cliente a la petición
        try:
            request.cliente = request.user.client_account
        except AttributeError:
            raise NotFound('Perfil de cliente no encontrado para este usuario.')

# api/clientes/views.py


class PerfilClienteView(ClienteBaseAPIView):
    def get(self, request):
        # 'request.cliente' ya está disponible automáticamente
        cliente = request.cliente 
        
        return Response({
            'id': cliente.id,
            'telefono': cliente.phone_number,
            'direccion': cliente.address, 
            "cedula": cliente.national_id
        })


class ReservasClienteView(ClienteBaseAPIView):
    def get(self, request):
        reservas = (
            ReservationDetail.objects
            .filter(
                reservation__client=request.cliente,
                reservation__invoice__isnull=False,
                package_id__in=TouristPackage.objects.values('id'),
            )
            .annotate(
                package_name=Subquery(
                    TouristPackage.objects
                    .filter(id=OuterRef('package_id'))
                    .values('name')[:1]
                ),
                package_description=Subquery(
                    TouristPackage.objects
                    .filter(id=OuterRef('package_id'))
                    .values('description')[:1]
                ),
            )
            .values(
                'reservation__client_id',
                'reservation_id',
                'reservation__client__name',
                'reservation__client__national_id',
                'reservation__invoice__invoice_number',
                'reservation__invoice__total',
                'reservation__payment_type__name',
                'package_name',
                'package_description',
            )
            .distinct()
        )

        return Response([
            {
                'id': reserva['reservation__client_id'],
                'idReserva': reserva['reservation_id'],
                'nombre': reserva['reservation__client__name'],
                'cedula': reserva['reservation__client__national_id'],
                'numero_factura': reserva['reservation__invoice__invoice_number'],
                'total': reserva['reservation__invoice__total'],
                'tipo_pago': reserva['reservation__payment_type__name'],
                'nombre_paquete': reserva['package_name'],
                'descripcion_paquete': reserva['package_description'],
            }
            for reserva in reservas
        ])