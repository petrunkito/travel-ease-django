from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.services.models import PriceHistory


class ServicePriceHistoryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='service_tester',
            email='service_tester@example.com',
            password='strong-pass-123',
        )
        self.client.force_authenticate(user=self.user)

    def test_create_flight_with_initial_price(self):
        response = self.client.post(
            '/api/services/flights/',
            {
                'airline': 'Avianca',
                'origin': 'Managua',
                'destination': 'Madrid',
                'departure_date': '2026-05-01T10:00:00Z',
                'arrival_date': '2026-05-01T20:00:00Z',
                'price': '300.00',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['current_price'], Decimal('300.00'))

        flight_id = response.data['id']
        active_price = PriceHistory.objects.get(
            service_type=PriceHistory.ServiceType.FLIGHT,
            service_id=flight_id,
            end_date__isnull=True,
        )
        self.assertEqual(active_price.price, Decimal('300.00'))

    def test_change_flight_price_closes_previous_row(self):
        create_response = self.client.post(
            '/api/services/flights/',
            {
                'airline': 'Avianca',
                'origin': 'Managua',
                'destination': 'Madrid',
                'departure_date': '2026-05-01T10:00:00Z',
                'arrival_date': '2026-05-01T20:00:00Z',
                'price': '300.00',
            },
            format='json',
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        flight_id = create_response.data['id']

        update_price_response = self.client.post(
            f'/api/services/flights/{flight_id}/prices/',
            {'price': '325.00'},
            format='json',
        )
        self.assertEqual(update_price_response.status_code, status.HTTP_201_CREATED)

        active_prices = PriceHistory.objects.filter(
            service_type=PriceHistory.ServiceType.FLIGHT,
            service_id=flight_id,
            end_date__isnull=True,
        )
        self.assertEqual(active_prices.count(), 1)
        self.assertEqual(active_prices.first().price, Decimal('325.00'))

        closed_prices = PriceHistory.objects.filter(
            service_type=PriceHistory.ServiceType.FLIGHT,
            service_id=flight_id,
            end_date__isnull=False,
        )
        self.assertEqual(closed_prices.count(), 1)
        self.assertEqual(closed_prices.first().price, Decimal('300.00'))
