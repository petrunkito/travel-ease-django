from django.db import models

from api.services.flights.models import Flight
from api.services.hotels.models import Hotel
from api.services.transportation.models import Transportation


class PriceHistory(models.Model):
	class ServiceType(models.TextChoices):
		FLIGHT = 'Vuelo', 'Flight'
		HOTEL = 'Hotel', 'Hotel'
		TRANSPORTATION = 'Transporte', 'Transportation'

	service_type = models.CharField(max_length=50, choices=ServiceType.choices, db_column='TipoServicio')
	service_id = models.BigIntegerField(db_column='IdServicio')
	price = models.DecimalField(max_digits=10, decimal_places=2, db_column='Precio')
	start_date = models.DateTimeField(db_column='FechaInicio')
	end_date = models.DateTimeField(db_column='FechaFin', null=True, blank=True)

	class Meta:
		db_table = 'HistorialPrecio'
		ordering = ['-start_date', '-id']
		indexes = [
			models.Index(fields=['service_type', 'service_id']),
			models.Index(fields=['service_type', 'service_id', 'end_date']),
		]

	def __str__(self):
		return f'{self.service_type} #{self.service_id} - {self.price}'

__all__ = ['Flight', 'Hotel', 'Transportation', 'PriceHistory']
