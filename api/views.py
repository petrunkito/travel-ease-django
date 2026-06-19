from decimal import Decimal

from django.db import connections
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def health_check(request):
	return Response({'status': 'ok', 'message': 'Travel Ease API is running'})


def _normalize_dw_value(value):
	if isinstance(value, Decimal):
		return f'{value:.2f}'
	return value


def _fetch_warehouse_view(view_name, columns, order_by):
	query = f"SELECT {', '.join(columns)} FROM dbo.{view_name} ORDER BY {order_by}"

	with connections['dw'].cursor() as cursor:
		cursor.execute(query)
		rows = cursor.fetchall()
		column_names = [column[0] for column in cursor.description]

	return [
		{
			column_name: _normalize_dw_value(value)
			for column_name, value in zip(column_names, row)
		}
		for row in rows
	]


@api_view(['GET'])
def warehouse_income_by_destination(request):
	data = _fetch_warehouse_view(
		'vw_IngresosPorDestino',
		['Pais', 'Ciudad', 'Ingresos'],
		'Ingresos DESC, Pais ASC, Ciudad ASC',
	)
	return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def warehouse_top_clients(request):
	data = _fetch_warehouse_view(
		'vw_TopClientes',
		['NombreCliente', 'TotalComprado'],
		'TotalComprado DESC, NombreCliente ASC',
	)
	return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def warehouse_top_packages(request):
	data = _fetch_warehouse_view(
		'vw_PaquetesMasVendidos',
		['NombrePaquete', 'TotalReservas'],
		'TotalReservas DESC, NombrePaquete ASC',
	)
	return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def warehouse_high_season(request):
	data = _fetch_warehouse_view(
		'vw_TemporadaAlta',
		['MesNombre', 'TotalVentas'],
		'TotalVentas DESC, MesNombre ASC',
	)
	return Response(data, status=status.HTTP_200_OK)
