from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, db_column='Nombre')
    code = models.CharField(max_length=20, db_column='Codigo', unique=True)

    class Meta:
        db_table = 'Departamento'
        ordering = ['id']

    def __str__(self):
        return f'{self.code} - {self.name}'
