from django.db import models

from api.catalogos.departamentos.models import Department


class Municipality(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='municipalities',
        db_column='IdDepartamento',
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'Municipio'
        ordering = ['id']

    def __str__(self):
        return f'{self.code} - {self.name}'
