from django.db import models

from api.catalogos.type_transport.models import TypeTransport


class Transportation(models.Model):
    type_transport = models.ForeignKey(
        TypeTransport,
        on_delete=models.PROTECT,
        related_name='transportations',
        db_column='IdTipoTransporte',
    )
    origin = models.CharField(max_length=100, db_column='Origen')
    destination = models.CharField(max_length=100, db_column='Destino')
    active = models.BooleanField(default=True, db_column='Activo')

    class Meta:
        db_table = 'Transporte'
        ordering = ['id']

    def __str__(self):
        return f'{self.type_transport.code} - {self.origin} -> {self.destination}'
