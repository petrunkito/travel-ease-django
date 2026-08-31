from django.conf import settings
from django.db import models


class Destination(models.Model):
    city = models.CharField(max_length=100, db_column='Ciudad')
    country = models.CharField(max_length=100, db_column='Pais')
    code = models.CharField(max_length=20, db_column='Codigo', unique=True, null=True, blank=True)
    active = models.BooleanField(default=True, db_column='Activo')

    class Meta:
        db_table = 'Destino'
        ordering = ['id']

    def __str__(self):
        return f'{self.city}, {self.country}'


class TouristPackage(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='tourist_packages',
        db_column='IdUsuario',
    )
    destination = models.ForeignKey(
        Destination,
        on_delete=models.PROTECT,
        related_name='tourist_packages',
        db_column='IdDestino',
    )
    name = models.CharField(max_length=100, null=True, blank=True, db_column='Nombre')
    description = models.CharField(max_length=250, null=True, blank=True, db_column='Descripcion')
    created_at = models.DateTimeField(auto_now_add=True, db_column='FechaCreacion')
    active = models.BooleanField(default=True, db_column='Activo')

    class Meta:
        db_table = 'PaqueteTuristico'
        ordering = ['id']

    def __str__(self):
        return f'{self.id} - {self.name}'


class PackageDetail(models.Model):
    class ServiceType(models.TextChoices):
        FLIGHT = 'Vuelo', 'Flight'
        HOTEL = 'Hotel', 'Hotel'
        TRANSPORTATION = 'Transporte', 'Transportation'

    package = models.ForeignKey(
        TouristPackage,
        on_delete=models.CASCADE,
        related_name='details',
        db_column='IdPaquete',
    )
    service_type = models.CharField(max_length=50, choices=ServiceType.choices, db_column='TipoServicio')
    service_id = models.BigIntegerField(db_column='IdServicio')
    quantity = models.IntegerField(db_column='Cantidad')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='PrecioUnitario')
    total = models.DecimalField(max_digits=10, decimal_places=2, db_column='Total')

    class Meta:
        db_table = 'DetallePaquete'
        ordering = ['id']

    def __str__(self):
        return f'{self.package_id} - {self.service_type} #{self.service_id}'
