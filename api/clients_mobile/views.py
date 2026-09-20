from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import OuterRef, Subquery

from api.packages.models import TouristPackage
from api.reservations.models import Reservation, ReservationDetail
from api.services.flights.models import Flight
from api.services.hotels.models import Hotel
from api.services.transportation.models import Transportation
from .serializers import SugerenciaSerializer, ValoracionSerializer

from django.conf import settings
from django.db import connections


from rest_framework.exceptions import APIException

from bson import json_util
import json


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


def _service_snapshot(detail):
    service_type = detail.service_type.strip().lower()

    if service_type in ('vuelo', 'flight'):
        service = get_object_or_404(Flight, pk=detail.service_id)
        return 'vuelo', {
            'origen': service.origin,
            'destino': service.destination,
        }

    if service_type in ('hotel',):
        service = get_object_or_404(Hotel, pk=detail.service_id)
        return 'hotel', {
            'nombre': service.name,
            'estrellas': service.stars,
        }

    if service_type in ('transporte', 'transportation'):
        service = get_object_or_404(
            Transportation.objects.select_related('type_transport'),
            pk=detail.service_id,
        )
        return 'transporte', {
            'origen': service.origin,
            'destino': service.destination,
            'tipo': service.type_transport.name,
        }

    raise ValidationError({'idReserva': 'La reserva contiene un tipo de servicio invalido.'})


class ValoracionClienteView(ClienteBaseAPIView):
    def post(self, request):
        serializer = ValoracionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reservation = get_object_or_404(
            Reservation.objects.prefetch_related('details'),
            pk=serializer.validated_data['idReserva'],
            client=request.cliente,
            active=True,
        )
        reservation_details = list(reservation.details.all())
        package_ids = {detail.package_id for detail in reservation_details if detail.package_id}
        if not package_ids:
            raise NotFound('La reserva no tiene un paquete turístico asociado.')
        if len(package_ids) > 1:
            raise ValidationError({'idReserva': 'La reserva contiene más de un paquete turístico.'})

        package = get_object_or_404(TouristPackage, pk=package_ids.pop())
        service_groups = {}
        for detail in reservation_details:
            service_key, service_data = _service_snapshot(detail)
            service_groups.setdefault(service_key, []).append(service_data)

        document = {
            'idCliente': reservation.client_id,
            'cedulaCliente': reservation.client.national_id,
            'nombreCliente': reservation.client.name,
            'numeroTelefono': reservation.client.phone_number,
            'idReserva': reservation.id,
            'puntaje': serializer.validated_data['puntaje'],
            'comentario': serializer.validated_data['comentario'],
            'nombre': package.name,
            'descripcion': package.description,
            'precio': float(reservation.total),
            **service_groups,
        }

        try:
            connection = connections['mongodb']
            connection.ensure_connection()
            database = connection.connection[settings.DATABASES['mongodb']['NAME']]
            result = database['valaracion'].insert_one(document)
        except Exception as error:
            return Response(
                {
                    'mensaje': 'Error al guardar la valoración en MongoDB.',
                    'detalle': str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                'mensaje': 'Valoración guardada correctamente.',
                'id': str(result.inserted_id),
            },
            status=status.HTTP_201_CREATED,
        )


class SugerenciaClienteView(ClienteBaseAPIView):
    def post(self, request):
        serializer = SugerenciaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cliente = request.cliente
        document = {
            'idCliente': cliente.id,
            'cedulaCliente': cliente.national_id,
            'nombreCliente': cliente.name,
            'numeroTelefono': cliente.phone_number,
            'comentario': serializer.validated_data['comentario'],
        }

        try:
            connection = connections['mongodb']
            connection.ensure_connection()
            database = connection.connection[settings.DATABASES['mongodb']['NAME']]
            result = database['sugerencias'].insert_one(document)
        except Exception as error:
            return Response(
                {
                    'mensaje': 'Error al guardar la sugerencia en MongoDB.',
                    'detalle': str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                'mensaje': 'Sugerencia guardada correctamente.',
                'id': str(result.inserted_id),
            },
            status=status.HTTP_201_CREATED,
        )

class MongoDBTestView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            # Obtener la conexión configurada en Django
            connection = connections["mongodb"]

            # Establecer la conexión
            connection.ensure_connection()

            # Obtener el cliente de MongoDB
            client = connection.connection

            # Verificar conectividad
            client.admin.command("ping")

            # Obtener la base de datos
            db = client[settings.DATABASES["mongodb"]["NAME"]]

            # Seleccionar la colección
            collection = db["opiniones"]

            # Consultar hasta 10 documentos
            documents = list(
                collection.find().limit(10)
            )

            # Convertir BSON a JSON
            documents_json = json.loads(
                json_util.dumps(documents)
            )

            return Response({
                "mensaje": "Conexión exitosa con MongoDB",
                "base_datos": db.name,
                "coleccion": collection.name,
                "cantidad": len(documents_json),
                "datos": documents_json
            })

        except Exception as e:
            return Response({
                "mensaje": "Error al conectar o consultar MongoDB",
                "detalle": str(e)
            }, status=500)






























