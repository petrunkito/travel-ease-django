from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.catalogos.departamentos.models import Department
from api.catalogos.municipios.models import Municipality
from .models import Client


class ClientAccountTests(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.user_model = get_user_model()
        self.employee = self.user_model.objects.create_user(
            username='employee',
            email='employee@example.com',
            password='employee-pass-123',
        )
        self.api_client.force_authenticate(user=self.employee)
        department = Department.objects.create(name='Managua', code='TEST-MAN')
        self.municipality = Municipality.objects.create(
            department=department,
            name='Managua Centro',
            code='TEST-MAN-01',
        )

    def client_payload(self, email='client@example.com'):
        return {
            'email': email,
            'municipality': self.municipality.id,
            'name': 'Cliente de prueba',
            'national_id': 'TEST-001',
            'address': 'Direccion de prueba',
            'phone_number': '88888888',
        }

    def test_creating_client_creates_linked_login_account(self):
        response = self.api_client.post('/api/clientes/', self.client_payload(), format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        client = Client.objects.get(pk=response.data['id'])
        client_user = self.user_model.objects.get(username='client@example.com')
        self.assertEqual(client.user, client_user)
        self.assertEqual(response.data['user_id'], client_user.id)
        self.assertEqual(response.data['user_email'], 'client@example.com')
        self.assertTrue(client_user.check_password('travelease123'))
        self.assertTrue(client_user.groups.filter(name='CLIENTE').exists())

        login_response = self.api_client.post(
            '/api/users/login/',
            {'username': 'client@example.com', 'password': 'travelease123'},
            format='json',
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_duplicate_client_email_is_rejected_without_creating_client(self):
        self.user_model.objects.create_user(
            username='existing@example.com',
            email='existing@example.com',
            password='existing-pass-123',
        )

        response = self.api_client.post(
            '/api/clientes/',
            self.client_payload('existing@example.com'),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Client.objects.filter(name='Cliente de prueba').exists())
        self.assertEqual(
            self.user_model.objects.filter(username='existing@example.com').count(),
            1,
        )

    def test_email_is_required_to_create_client(self):
        payload = self.client_payload()
        payload.pop('email')

        response = self.api_client.post('/api/clientes/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Client.objects.filter(name='Cliente de prueba').exists())
