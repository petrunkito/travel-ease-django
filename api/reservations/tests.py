from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.clients.models import Client
from api.catalogos.departamentos.models import Department
from api.catalogos.municipios.models import Municipality
from api.packages.models import TouristPackage, PackageDetail, Destination
from .models import (
    Reservation, ReservationStatus, PaymentType,
    ReservationDetail, ReservationStatusHistory, Invoice
)


class ReservationModelTests(TestCase):
    """Tests para los modelos de reservations."""

    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crear estados de reserva
        ReservationStatus.objects.get_or_create(
            code='PEND',
            defaults={'name': 'Pendiente'}
        )
        ReservationStatus.objects.get_or_create(
            code='PAG',
            defaults={'name': 'Pagado'}
        )
        ReservationStatus.objects.get_or_create(
            code='CANC',
            defaults={'name': 'Cancelado'}
        )

        # Crear tipo de pago
        PaymentType.objects.get_or_create(
            code='EFEC',
            defaults={'name': 'EFECTIVO', 'active': True}
        )
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

        self.department, _ = Department.objects.get_or_create(
            code='MAN',
            defaults={'name': 'Managua'}
        )

        self.municipality, _ = Municipality.objects.get_or_create(
            code='MAN-01',
            defaults={
                'department': self.department,
                'name': 'Managua'
            }
        )

        self.client = Client.objects.create(
            municipality=self.municipality,
            created_by=self.user,
            name='Juan Perez',
            national_id='0010203031234R',
            address='Calle Principal 123',
            phone_number='88888888'
        )

        self.destination = Destination.objects.create(
            city='Granada',
            country='Nicaragua',
            code='GRA-01'
        )

        self.package = TouristPackage.objects.create(
            created_by=self.user,
            destination=self.destination,
            name='Tour a Granada',
            description='Visita a Granada',
            active=True
        )

        self.payment_type = PaymentType.objects.get(code='EFEC')
        self.status_pending = ReservationStatus.objects.get(code='PEND')

    def test_create_reservation(self):
        """Test para crear una reserva."""
        reservation = Reservation.objects.create(
            client=self.client,
            payment_type=self.payment_type,
            seller_user=self.user,
            total=500.00
        )
        self.assertEqual(reservation.client.name, 'Juan Perez')
        self.assertEqual(reservation.total, 500.00)
        self.assertTrue(reservation.active)

    def test_create_reservation_status_history(self):
        """Test para crear historial de estados."""
        reservation = Reservation.objects.create(
            client=self.client,
            payment_type=self.payment_type,
            seller_user=self.user,
            total=500.00
        )

        history = ReservationStatusHistory.objects.create(
            reservation=reservation,
            status=self.status_pending
        )

        self.assertEqual(history.reservation, reservation)
        self.assertEqual(history.status.code, 'PEND')


class ReservationAPITests(APITestCase):
    """Tests para los endpoints de reservations."""

    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crear estados de reserva
        ReservationStatus.objects.get_or_create(
            code='PEND',
            defaults={'name': 'Pendiente'}
        )
        ReservationStatus.objects.get_or_create(
            code='PAG',
            defaults={'name': 'Pagado'}
        )
        ReservationStatus.objects.get_or_create(
            code='CANC',
            defaults={'name': 'Cancelado'}
        )

        # Crear tipo de pago
        PaymentType.objects.get_or_create(
            code='EFEC',
            defaults={'name': 'EFECTIVO', 'active': True}
        )
        
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

        self.department, _ = Department.objects.get_or_create(
            code='MAN',
            defaults={'name': 'Managua'}
        )

        self.municipality, _ = Municipality.objects.get_or_create(
            code='MAN-01',
            defaults={
                'department': self.department,
                'name': 'Managua'
            }
        )

        self.django_client = Client.objects.create(
            municipality=self.municipality,
            created_by=self.user,
            name='Juan Perez',
            national_id='0010203031234R',
            address='Calle Principal 123',
            phone_number='88888888'
        )

        self.destination = Destination.objects.create(
            city='Granada',
            country='Nicaragua',
            code='GRA-01'
        )

        self.package = TouristPackage.objects.create(
            created_by=self.user,
            destination=self.destination,
            name='Tour a Granada',
            description='Visita a Granada',
            active=True
        )

        # Agregar detalles al paquete
        PackageDetail.objects.create(
            package=self.package,
            service_type='VUELO',
            service_id=1,
            quantity=2,
            unit_price=150.00,
            total=300.00
        )

        self.payment_type = PaymentType.objects.get(code='EFEC')

    def test_list_payment_types(self):
        """Test para listar tipos de pago."""
        response = self.client.get('/api/reservations/payment-types/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_list_reservation_statuses(self):
        """Test para listar estados de reserva."""
        response = self.client.get('/api/reservations/reservation-statuses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_reservation(self):
        """Test para crear una reserva."""
        data = {
            'client_id': self.django_client.id,
            'package_id': self.package.id,
            'payment_type_id': self.payment_type.id,
            'seller_user_id': self.user.id
        }
        response = self.client.post('/api/reservations/reservations/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['client'], self.django_client.id)
        self.assertEqual(response.data['total'], '300.00')
        
        # Verificar que la factura se creó automáticamente
        self.assertIsNotNone(response.data['invoice'])
        self.assertIn('FAC-', response.data['invoice']['invoice_number'])

    def test_list_reservations(self):
        """Test para listar reservas."""
        # Crear una reserva primero
        Reservation.objects.create(
            client=self.django_client,
            payment_type=self.payment_type,
            seller_user=self.user,
            total=300.00
        )

        response = self.client.get('/api/reservations/reservations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_reservation_detail(self):
        """Test para obtener detalle de una reserva."""
        reservation = Reservation.objects.create(
            client=self.django_client,
            payment_type=self.payment_type,
            seller_user=self.user,
            total=300.00
        )

        response = self.client.get(f'/api/reservations/reservations/{reservation.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], reservation.id)

    def test_update_reservation_status(self):
        """Test para cambiar el estado de una reserva."""
        reservation = Reservation.objects.create(
            client=self.django_client,
            payment_type=self.payment_type,
            seller_user=self.user,
            total=300.00
        )

        # Crear estado inicial
        status_pending = ReservationStatus.objects.get(code='PEND')
        ReservationStatusHistory.objects.create(
            reservation=reservation,
            status=status_pending
        )

        # Cambiar a Pagado
        status_paid = ReservationStatus.objects.get(code='PAG')
        data = {'status_id': status_paid.id}
        response = self.client.put(f'/api/reservations/reservations/{reservation.id}/update_status/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_update_paid_reservation(self):
        """Test que no permite cambiar el estado de una reserva ya pagada."""
        reservation = Reservation.objects.create(
            client=self.django_client,
            payment_type=self.payment_type,
            seller_user=self.user,
            total=300.00
        )

        # Crear estado pagado
        status_paid = ReservationStatus.objects.get(code='PAG')
        ReservationStatusHistory.objects.create(
            reservation=reservation,
            status=status_paid
        )

        # Intentar cambiar el estado
        status_cancelled = ReservationStatus.objects.get(code='CANC')
        data = {'status_id': status_cancelled.id}
        response = self.client.put(f'/api/reservations/reservations/{reservation.id}/update_status/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invoice_created_automatically(self):
        """Test que la factura se crea automáticamente con la reserva."""
        # Crear una reserva
        data = {
            'client_id': self.django_client.id,
            'package_id': self.package.id,
            'payment_type_id': self.payment_type.id,
            'seller_user_id': self.user.id
        }
        response = self.client.post('/api/reservations/reservations/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que la factura existe
        reservation_id = response.data['id']
        invoice = Invoice.objects.get(reservation_id=reservation_id)
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.total, 300.00)

    def test_delete_reservation(self):
        """Test para desactivar una reserva."""
        reservation = Reservation.objects.create(
            client=self.django_client,
            payment_type=self.payment_type,
            seller_user=self.user,
            total=300.00
        )

        response = self.client.delete(f'/api/reservations/reservations/{reservation.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verificar que la reserva fue desactivada
        reservation.refresh_from_db()
        self.assertFalse(reservation.active)
