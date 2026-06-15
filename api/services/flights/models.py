from django.db import models


class Flight(models.Model):
    airline = models.CharField(max_length=100, db_column='Aerolinea')
    origin = models.CharField(max_length=100, db_column='Origen')
    destination = models.CharField(max_length=100, db_column='Destino')
    departure_date = models.DateTimeField(db_column='FechaSalida')
    arrival_date = models.DateTimeField(db_column='FechaLlegada')
    active = models.BooleanField(default=True, db_column='Activo')

    class Meta:
        db_table = 'Vuelo'
        ordering = ['id']

    def __str__(self):
        return f'{self.airline} - {self.origin} -> {self.destination}'
