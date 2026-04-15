from django.db import models


class TypeTransport(models.Model):
    name = models.CharField(max_length=50, db_column='Nombre', null=True, blank=True)
    code = models.CharField(max_length=20, db_column='Codigo', unique=True)
    active = models.BooleanField(default=True, db_column='Activo')

    class Meta:
        db_table = 'TipoTransporte'
        ordering = ['id']

    def __str__(self):
        return f'{self.code} - {self.name}'
