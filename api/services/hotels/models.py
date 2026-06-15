from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=100, db_column='Nombre')
    city = models.CharField(max_length=100, db_column='Ciudad')
    stars = models.IntegerField(db_column='Estrellas', null=True, blank=True)
    category = models.CharField(max_length=50, db_column='Categoria', null=True, blank=True)
    active = models.BooleanField(default=True, db_column='Activo')

    class Meta:
        db_table = 'Hotel'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} ({self.city})'
