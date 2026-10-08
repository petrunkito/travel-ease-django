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
