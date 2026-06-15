from django.db import models
from django.contrib.auth.models import User
from api.clients.models import Client


class PaymentType(models.Model):
    """Tipos de pago disponibles para las reservas."""
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'TipoPago'
        verbose_name = 'Tipo de Pago'
        verbose_name_plural = 'Tipos de Pago'

    def __str__(self):
        return f"{self.name} ({self.code})"


class ReservationStatus(models.Model):
    """Estados posibles de una reserva."""
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'EstadoReserva'
        verbose_name = 'Estado de Reserva'
        verbose_name_plural = 'Estados de Reserva'

    def __str__(self):
        return f"{self.name} ({self.code})"


class Reservation(models.Model):
    """Representa una reserva realizada por un cliente."""
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='reservations')
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT)
    seller_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reservations_sold')
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

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

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='details')
    package_id = models.IntegerField(null=True, blank=True)  # Referencia al paquete turístico
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    service_id = models.IntegerField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'DetalleReserva'
        verbose_name = 'Detalle de Reserva'
        verbose_name_plural = 'Detalles de Reserva'

    def __str__(self):
        return f"Detalle #{self.id} - {self.get_service_type_display()}"


class ReservationStatusHistory(models.Model):
    """Historial de cambios de estado de una reserva."""
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='status_history')
    status = models.ForeignKey(ReservationStatus, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'HistorialEstadoReserva'
        verbose_name = 'Historial Estado Reserva'
        verbose_name_plural = 'Historiales Estados Reservas'

    def __str__(self):
        return f"Historial #{self.id} - {self.status.name}"


class Invoice(models.Model):
    """Factura generada para una reserva."""
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50)
    issue_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Factura'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'

    def __str__(self):
        return f"Factura #{self.invoice_number}"
