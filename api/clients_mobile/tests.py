from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.catalogos.departamentos.models import Department
from api.catalogos.municipios.models import Municipality
from api.clients.models import Client
from api.reservations.models import Invoice, PaymentType, Reservation


class ClientReservationsViewTests(TestCase):
	def setUp(self):
		self.api_client = APIClient()
		user_model = get_user_model()
		self.user = user_model.objects.create_user(
			username='mobile-client',
			password='client-pass-123',
		)
		Group.objects.create(name='Cliente').user_set.add(self.user)
		department = Department.objects.create(name='Managua', code='MOBILE-MAN')
		municipality = Municipality.objects.create(
			department=department,
			name='Managua Centro',
			code='MOBILE-MAN-01',
		)
		self.client_account = Client.objects.create(
			user=self.user,
			municipality=municipality,
			created_by=self.user,
			name='Cliente movil',
			national_id='MOBILE-001',
		)
		self.payment_type = PaymentType.objects.create(name='Efectivo', code='MOBILE-EFEC')
		self.api_client.force_authenticate(user=self.user)

	def test_returns_only_client_reservations_with_invoice(self):
		reservation = Reservation.objects.create(
			client=self.client_account,
			payment_type=self.payment_type,
			seller_user=self.user,
			total=Decimal('125.50'),
		)
		Invoice.objects.create(
			reservation=reservation,
			invoice_number='FAC-MOBILE-001',
			total=Decimal('125.50'),
		)
		Reservation.objects.create(
			client=self.client_account,
			payment_type=self.payment_type,
			seller_user=self.user,
			total=Decimal('80.00'),
		)

		response = self.api_client.get('/api/clients-mobile/reservas/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, [{
			'id': self.client_account.id,
			'nombre': 'Cliente movil',
			'cedula': 'MOBILE-001',
			'numero_factura': 'FAC-MOBILE-001',
			'total': '125.50',
			'tipo_pago': 'Efectivo',
		}])
