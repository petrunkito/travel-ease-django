from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField


class Sugerencia(models.Model):
	id = ObjectIdAutoField(primary_key=True)
	client_id = models.IntegerField(db_column='idCliente')
	client_national_id = models.CharField(
		max_length=20,
		db_column='cedulaCliente',
		null=True,
		blank=True,
	)
	client_name = models.CharField(
		max_length=100,
		db_column='nombreCliente',
		null=True,
		blank=True,
	)
	client_phone_number = models.CharField(
		max_length=20,
		db_column='numeroTelefono',
		null=True,
		blank=True,
	)
	comment = models.CharField(max_length=1000, db_column='comentario')

	class Meta:
		db_table = 'sugerencias'
		managed = False


class SatisfactionSurvey(models.Model):
	id = ObjectIdAutoField(primary_key=True)
	client_id = models.IntegerField(db_column='idCliente')
	client_national_id = models.CharField(
		max_length=20,
		db_column='cedulaCliente',
		null=True,
		blank=True,
	)
	client_name = models.CharField(
		max_length=100,
		db_column='nombreCliente',
		null=True,
		blank=True,
	)
	client_phone_number = models.CharField(
		max_length=20,
		db_column='numeroTelefono',
		null=True,
		blank=True,
	)
	reservation_id = models.IntegerField(
		db_column='idReserva',
		null=True,
		blank=True,
	)
	customer_service = models.IntegerField(db_column='atencionAlCliente')
	reservation_ease = models.IntegerField(db_column='facilidadReserva')
	value_for_money = models.IntegerField(db_column='relacionCalidadPrecio')
	service_quality = models.IntegerField(db_column='calidadServicioProporcionado')
	favorite_feature = models.CharField(max_length=1000, db_column='caracteristicaFav')
	simple_information = models.BooleanField(db_column='informacionProporcionadaSencilla')
	recommend_to_others = models.BooleanField(db_column='recomendarAOtros')
	would_hire_again = models.BooleanField(db_column='volverContratar')

	class Meta:
		db_table = 'encuestaSatisfaccion'
		managed = False


class Valoracion(models.Model):
	id = ObjectIdAutoField(primary_key=True)
	client_id = models.IntegerField(db_column='idCliente')
	client_national_id = models.CharField(
		max_length=20,
		db_column='cedulaCliente',
		null=True,
		blank=True,
	)
	client_name = models.CharField(
		max_length=100,
		db_column='nombreCliente',
		null=True,
		blank=True,
	)
	client_phone_number = models.CharField(
		max_length=20,
		db_column='numeroTelefono',
		null=True,
		blank=True,
	)
	reservation_id = models.IntegerField(db_column='idReserva')
	score = models.IntegerField(db_column='puntaje')
	comment = models.CharField(max_length=1000, db_column='comentario')
	package_name = models.CharField(max_length=255, db_column='nombre', null=True, blank=True)
	package_description = models.TextField(db_column='descripcion', null=True, blank=True)
	price = models.DecimalField(max_digits=12, decimal_places=2, db_column='precio')
	flight = models.JSONField(db_column='vuelo', null=True, blank=True)
	hotel = models.JSONField(db_column='hotel', null=True, blank=True)
	transportation = models.JSONField(db_column='transporte', null=True, blank=True)

	class Meta:
		db_table = 'valaracion'
		managed = False
