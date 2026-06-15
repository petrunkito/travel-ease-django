from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.catalogos.type_transport.models import TypeTransport
from api.packages.models import Destination, PackageDetail, TouristPackage
from api.services.flights.models import Flight
from api.services.hotels.models import Hotel
from api.services.models import PriceHistory
from api.services.pricing import set_service_price
from api.services.transportation.models import Transportation


class TouristPackageTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='package_tester',
            email='package_tester@example.com',
            password='strong-pass-123',
        )
        self.client.force_authenticate(user=self.user)

        self.flight = Flight.objects.create(
            airline='Avianca',
            origin='Managua',
            destination='Madrid',
            departure_date='2026-05-01T10:00:00Z',
            arrival_date='2026-05-01T20:00:00Z',
        )
        set_service_price(PriceHistory.ServiceType.FLIGHT, self.flight.id, '300.00')

        self.hotel = Hotel.objects.create(
            name='Hotel Centro',
            city='Madrid',
            stars=4,
            category='Business',
        )
        set_service_price(PriceHistory.ServiceType.HOTEL, self.hotel.id, '150.00')

        self.type_transport = TypeTransport.objects.create(name='Taxi', code='TAXI')
        self.transportation = Transportation.objects.create(
            type_transport=self.type_transport,
            origin='Aeropuerto',
            destination='Hotel',
        )
        set_service_price(PriceHistory.ServiceType.TRANSPORTATION, self.transportation.id, '25.00')

    def test_create_package_with_services(self):
        response = self.client.post(
            '/api/packages/',
            {
                'destination': {
                    'city': 'Madrid',
                    'country': 'España',
                },
                'name': 'Viaje Madrid',
                'description': 'Paquete completo',
                'details': [
                    {
                        'service_type': PriceHistory.ServiceType.FLIGHT,
                        'service_id': self.flight.id,
                        'quantity': 1,
                    },
                    {
                        'service_type': PriceHistory.ServiceType.HOTEL,
                        'service_id': self.hotel.id,
                        'quantity': 2,
                    },
                    {
                        'service_type': PriceHistory.ServiceType.TRANSPORTATION,
                        'service_id': self.transportation.id,
                        'quantity': 1,
                    },
                ],
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['destination']['city'], 'Madrid')
        self.assertEqual(len(response.data['services']['flights']), 1)
        self.assertEqual(len(response.data['services']['hotels']), 1)
        self.assertEqual(len(response.data['services']['transportation']), 1)

        package = TouristPackage.objects.get(pk=response.data['id'])
        self.assertTrue(package.active)
        self.assertEqual(package.details.count(), 3)

    def test_update_package_details_replaces_removed_items(self):
        create_response = self.client.post(
            '/api/packages/',
            {
                'destination': {
                    'city': 'Madrid',
                    'country': 'España',
                },
                'name': 'Viaje Madrid',
                'description': 'Paquete inicial',
                'details': [
                    {
                        'service_type': PriceHistory.ServiceType.FLIGHT,
                        'service_id': self.flight.id,
                        'quantity': 1,
                    },
                    {
                        'service_type': PriceHistory.ServiceType.HOTEL,
                        'service_id': self.hotel.id,
                        'quantity': 1,
                    },
                ],
            },
            format='json',
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        package_id = create_response.data['id']
        package = TouristPackage.objects.get(pk=package_id)
        hotel_detail = package.details.get(service_type=PriceHistory.ServiceType.HOTEL)

        update_response = self.client.patch(
            f'/api/packages/{package_id}/',
            {
                'destination': {
                    'city': 'Barcelona',
                    'country': 'España',
                },
                'details': [
                    {
                        'id': hotel_detail.id,
                        'service_type': PriceHistory.ServiceType.HOTEL,
                        'service_id': self.hotel.id,
                        'quantity': 3,
                    },
                    {
                        'service_type': PriceHistory.ServiceType.TRANSPORTATION,
                        'service_id': self.transportation.id,
                        'quantity': 1,
                    },
                ],
            },
            format='json',
        )

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        package.refresh_from_db()
        self.assertEqual(package.destination.city, 'Barcelona')
        self.assertEqual(package.details.count(), 2)
        self.assertFalse(package.details.filter(service_type=PriceHistory.ServiceType.FLIGHT).exists())
        self.assertTrue(package.details.filter(service_type=PriceHistory.ServiceType.TRANSPORTATION).exists())

    def test_delete_package_is_logical(self):
        create_response = self.client.post(
            '/api/packages/',
            {
                'destination': {
                    'city': 'Madrid',
                    'country': 'España',
                },
                'name': 'Viaje Madrid',
                'description': 'Paquete para eliminar',
                'details': [
                    {
                        'service_type': PriceHistory.ServiceType.FLIGHT,
                        'service_id': self.flight.id,
                        'quantity': 1,
                    },
                ],
            },
            format='json',
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        delete_response = self.client.delete(f"/api/packages/{create_response.data['id']}/")
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)

        package = TouristPackage.objects.get(pk=create_response.data['id'])
        self.assertFalse(package.active)
