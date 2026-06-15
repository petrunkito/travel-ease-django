from django.conf import settings
from django.db import models

from api.catalogos.municipios.models import Municipality


class Client(models.Model):
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.PROTECT,
        related_name='clients',
        db_column='IdMunicipio',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='registered_clients',
        db_column='IdUsuarioRegistro',
    )
    name = models.CharField(max_length=100, null=True, blank=True, db_column='Nombre')
    national_id = models.CharField(max_length=20, null=True, blank=True, db_column='Cedula')
    address = models.CharField(max_length=250, null=True, blank=True, db_column='Direccion')
    phone_number = models.CharField(max_length=20, null=True, blank=True, db_column='Numero')
    registration_date = models.DateTimeField(auto_now_add=True, db_column='FechaRegistro')
    active = models.BooleanField(default=True, db_column='Activo')

    class Meta:
        db_table = 'Cliente'
        ordering = ['id']

    def __str__(self):
        return f'{self.id} - {self.name}'
