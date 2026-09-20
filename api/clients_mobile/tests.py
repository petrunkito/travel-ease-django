from decimal import Decimal
from unittest.mock import MagicMock, patch

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

	def test_creates_satisfaction_survey_in_mongodb(self):
		reservation = Reservation.objects.create(
			client=self.client_account,
			payment_type=self.payment_type,
			seller_user=self.user,
			total=Decimal('125.50'),
		)
		mongo_connection = MagicMock()
		mongo_database = MagicMock()
		mongo_collection = MagicMock()
		mongo_collection.insert_one.return_value.inserted_id = 'survey-id'
		mongo_connection.connection = {'TravelEase': mongo_database}
		mongo_database.__getitem__.return_value = mongo_collection

		payload = {
			'atencionAlCliente': 4,
			'facilidadReserva': 4,
			'relacionCalidadPrecio': 5,
			'calidadServicioProporcionado': 5,
			'caracteristicaFav': 'Buen catálogo.',
			'informacionProporcionadaSencilla': 1,
			'recomendarAOtros': 1,
			'volverContratar': 1,
		}

		with patch('api.clients_mobile.views.connections') as connections:
			connections.__getitem__.return_value = mongo_connection
			response = self.api_client.post(
				'/api/clients-mobile/encuesta-satisfaccion/',
				payload,
				format='json',
			)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data['idReserva'], reservation.id)
		mongo_database.__getitem__.assert_called_once_with('encuestaSatisfaccion')
		mongo_collection.insert_one.assert_called_once()
		self.assertEqual(
			mongo_collection.insert_one.call_args.args[0]['idCliente'],
			self.client_account.id,
		)
		self.assertEqual(
			mongo_collection.insert_one.call_args.args[0]['recomendarAOtros'],
			True,
		)
