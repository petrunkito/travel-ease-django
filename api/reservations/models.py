from django.db import models
from django.contrib.auth.models import User
from api.clients.models import Client


class PaymentType(models.Model):
    """Tipos de pago disponibles para las reservas."""
    name = models.CharField(max_length=50, db_column='Nombre')
    code = models.CharField(max_length=20, db_column='Codigo', unique=True)

    class Meta:
        db_table = 'TipoPago'
        verbose_name = 'Tipo de Pago'
        verbose_name_plural = 'Tipos de Pago'

    def __str__(self):
        return f"{self.name} ({self.code})"


class ReservationStatus(models.Model):
    """Estados posibles de una reserva."""
    name = models.CharField(max_length=50, db_column='Nombre')
    code = models.CharField(max_length=20, db_column='Codigo', unique=True)

    class Meta:
        db_table = 'EstadoReserva'
        verbose_name = 'Estado de Reserva'
        verbose_name_plural = 'Estados de Reserva'

    def __str__(self):
        return f"{self.name} ({self.code})"


class Reservation(models.Model):
    """Representa una reserva realizada por un cliente."""
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='reservations', db_column='IdCliente')
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT, db_column='IdTipoPago')
    seller_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='reservations_sold',
        db_column='IdUsuarioVendedor',
    )
    date = models.DateTimeField(auto_now_add=True, db_column='Fecha')
    total = models.DecimalField(max_digits=10, decimal_places=2, db_column='Total')
    active = models.BooleanField(default=True, db_column='Activo')

    class Meta:
        db_table = 'Reserva'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"Reserva #{self.id} - Cliente: {self.client.name}"


class ReservationDetail(models.Model):
    """Detalle de los servicios incluidos en una reserva."""
    SERVICE_TYPES = [
        ('VUELO', 'Vuelo'),
        ('HOTEL', 'Hotel'),
        ('TRANSPORTE', 'Transporte'),
    ]

    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='details',
        db_column='IdReserva',
    )
    package_id = models.IntegerField(db_column='IdPaquete', null=True, blank=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES, db_column='TipoServicio')
    service_id = models.IntegerField(db_column='IdServicio')
    quantity = models.IntegerField(db_column='Cantidad')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='PrecioUnitario')
    total = models.DecimalField(max_digits=10, decimal_places=2, db_column='Total')

    class Meta:
        db_table = 'DetalleReserva'
        verbose_name = 'Detalle de Reserva'
        verbose_name_plural = 'Detalles de Reserva'

    def __str__(self):
        return f"Detalle #{self.id} - {self.get_service_type_display()}"


class ReservationStatusHistory(models.Model):
    """Historial de cambios de estado de una reserva."""
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='status_history',
        db_column='IdReserva',
    )
    status = models.ForeignKey(ReservationStatus, on_delete=models.PROTECT, db_column='IdEstado')
    date = models.DateTimeField(auto_now_add=True, db_column='Fecha')

    class Meta:
        db_table = 'HistorialEstadoReserva'
        verbose_name = 'Historial Estado Reserva'
        verbose_name_plural = 'Historiales Estados Reservas'

    def __str__(self):
        return f"Historial #{self.id} - {self.status.name}"


class Invoice(models.Model):
    """Factura generada para una reserva."""
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='invoice',
        db_column='IdReserva',
    )
    invoice_number = models.CharField(max_length=50, db_column='NumeroFactura')
    issue_date = models.DateTimeField(auto_now_add=True, db_column='FechaEmision')
    total = models.DecimalField(max_digits=10, decimal_places=2, db_column='Total')

    class Meta:
        db_table = 'Factura'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'

    def __str__(self):
        return f"Factura #{self.invoice_number}"
