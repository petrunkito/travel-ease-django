from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.catalogos.departamentos.models import Department
from api.catalogos.municipios.models import Municipality
from api.clients.models import Client
from api.packages.models import Destination, TouristPackage
from api.reservations.models import Invoice, PaymentType, Reservation, ReservationDetail


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

	@patch('api.clients_mobile.views.SatisfactionSurvey.objects')
	def test_creates_satisfaction_survey_with_mongodb_orm(self, objects):
		reservation = Reservation.objects.create(
			client=self.client_account,
			payment_type=self.payment_type,
			seller_user=self.user,
			total=Decimal('125.50'),
		)
		manager = objects.using.return_value
		survey = manager.create.return_value
		survey.pk = 'survey-id'

		payload = {
			'idReserva': reservation.id,
			'atencionAlCliente': 4,
			'facilidadReserva': 4,
			'relacionCalidadPrecio': 5,
			'calidadServicioProporcionado': 5,
			'caracteristicaFav': 'Buen catálogo.',
			'informacionProporcionadaSencilla': 1,
			'recomendarAOtros': 1,
			'volverContratar': 1,
		}

		response = self.api_client.post(
			'/api/clients-mobile/encuesta-satisfaccion/',
			payload,
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data, {
			'mensaje': 'Encuesta de satisfacción guardada correctamente.',
			'id': 'survey-id',
		})
		objects.using.assert_called_once_with('mongodb')
		manager.create.assert_called_once_with(
			client_id=self.client_account.id,
			client_national_id=self.client_account.national_id,
			client_name=self.client_account.name,
			client_phone_number=self.client_account.phone_number,
			reservation_id=reservation.id,
			customer_service=4,
			reservation_ease=4,
			value_for_money=5,
			service_quality=5,
			favorite_feature='Buen catálogo.',
			simple_information=True,
			recommend_to_others=True,
			would_hire_again=True,
		)

	@patch('api.clients_mobile.views.Sugerencia.objects')
	def test_creates_suggestion_with_mongodb_orm(self, objects):
		manager = objects.using.return_value
		suggestion = manager.create.return_value
		suggestion.pk = 'suggestion-id'

		response = self.api_client.post(
			'/api/clients-mobile/sugerencias/',
			{'comentario': 'Excelente atención.'},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data, {
			'mensaje': 'Sugerencia guardada correctamente.',
			'id': 'suggestion-id',
		})
		objects.using.assert_called_once_with('mongodb')
		manager.create.assert_called_once_with(
			client_id=self.client_account.id,
			client_national_id=self.client_account.national_id,
			client_name=self.client_account.name,
			client_phone_number=self.client_account.phone_number,
			comment='Excelente atención.',
		)

	@patch('api.clients_mobile.views._service_snapshot')
	@patch('api.clients_mobile.views.Valoracion.objects')
	def test_creates_valuation_with_mongodb_orm(self, objects, service_snapshot):
		destination = Destination.objects.create(
			city='Managua',
			country='Nicaragua',
			code='MOBILE-DEST',
		)
		package = TouristPackage.objects.create(
			created_by=self.user,
			destination=destination,
			name='Paquete móvil',
			description='Paquete para valoración',
		)
		reservation = Reservation.objects.create(
			client=self.client_account,
			payment_type=self.payment_type,
			seller_user=self.user,
			total=Decimal('125.50'),
		)
		ReservationDetail.objects.create(
			reservation=reservation,
			package_id=package.id,
			service_type='Vuelo',
			service_id=1,
			quantity=1,
			unit_price=Decimal('125.50'),
			total=Decimal('125.50'),
		)
		service_snapshot_data = {'origen': 'Managua', 'destino': 'Madrid'}
		service_snapshot.return_value = ('vuelo', service_snapshot_data)
		manager = objects.using.return_value
		valuation = manager.create.return_value
		valuation.pk = 'valuation-id'

		response = self.api_client.post(
			'/api/clients-mobile/valoracion/',
			{
				'idReserva': reservation.id,
				'puntaje': 5,
				'comentario': 'Excelente servicio.',
			},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data, {
			'mensaje': 'Valoración guardada correctamente.',
			'id': 'valuation-id',
		})
		objects.using.assert_called_once_with('mongodb')
		manager.create.assert_called_once_with(
			client_id=self.client_account.id,
			client_national_id=self.client_account.national_id,
			client_name=self.client_account.name,
			client_phone_number=self.client_account.phone_number,
			reservation_id=reservation.id,
			score=5,
			comment='Excelente servicio.',
			package_name='Paquete móvil',
			package_description='Paquete para valoración',
			price=Decimal('125.50'),
			flight=[service_snapshot_data],
			hotel=None,
			transportation=None,
		)
