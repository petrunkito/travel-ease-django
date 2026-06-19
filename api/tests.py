from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase


class WarehouseEndpointsTests(APITestCase):
	def test_income_by_destination_endpoint(self):
		mock_data = [
			{'Pais': 'Panamá', 'Ciudad': 'Bocas del Toro', 'Ingresos': '10200.00'},
			{'Pais': 'Panamá', 'Ciudad': 'Portobelo', 'Ingresos': '7800.00'},
		]

		with patch('api.views._fetch_warehouse_view', return_value=mock_data) as mocked_fetch:
			response = self.client.get('/api/warehouse/ingresos-por-destino/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, mock_data)
		mocked_fetch.assert_called_once_with(
			'vw_IngresosPorDestino',
			['Pais', 'Ciudad', 'Ingresos'],
			'Ingresos DESC, Pais ASC, Ciudad ASC',
		)

	def test_top_clients_endpoint(self):
		mock_data = [
			{'NombreCliente': 'Ana López', 'TotalComprado': '7585.00'},
			{'NombreCliente': 'Andrés Castillo', 'TotalComprado': '5785.00'},
		]

		with patch('api.views._fetch_warehouse_view', return_value=mock_data) as mocked_fetch:
			response = self.client.get('/api/warehouse/top-clientes/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, mock_data)
		mocked_fetch.assert_called_once_with(
			'vw_TopClientes',
			['NombreCliente', 'TotalComprado'],
			'TotalComprado DESC, NombreCliente ASC',
		)

	def test_top_packages_endpoint(self):
		mock_data = [
			{'NombrePaquete': 'Bocas del Toro Beach', 'TotalReservas': 12},
			{'NombrePaquete': 'Buceo en Roatán', 'TotalReservas': 12},
		]

		with patch('api.views._fetch_warehouse_view', return_value=mock_data) as mocked_fetch:
			response = self.client.get('/api/warehouse/paquetes-mas-vendidos/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, mock_data)
		mocked_fetch.assert_called_once_with(
			'vw_PaquetesMasVendidos',
			['NombrePaquete', 'TotalReservas'],
			'TotalReservas DESC, NombrePaquete ASC',
		)

	def test_high_season_endpoint(self):
		mock_data = [
			{'MesNombre': 'January', 'TotalVentas': '19370.00'},
			{'MesNombre': 'February', 'TotalVentas': '17240.00'},
		]

		with patch('api.views._fetch_warehouse_view', return_value=mock_data) as mocked_fetch:
			response = self.client.get('/api/warehouse/temporada-alta/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, mock_data)
		mocked_fetch.assert_called_once_with(
			'vw_TemporadaAlta',
			['MesNombre', 'TotalVentas'],
			'TotalVentas DESC, MesNombre ASC',
		)
