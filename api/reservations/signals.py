from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import ReservationStatus, PaymentType


@receiver(post_migrate)
def create_default_statuses_and_payment_types(sender, **kwargs):
    """
    Crea los estados de reserva y tipos de pago por defecto
    después de que se ejecuten las migraciones.
    """
    if sender.name == 'api.reservations':
        # Crear estados de reserva
        statuses = [
            {'name': 'Pendiente', 'code': 'PEND'},
            {'name': 'Pagado', 'code': 'PAG'},
            {'name': 'Cancelado', 'code': 'CANC'},
        ]

        for status_data in statuses:
            ReservationStatus.objects.get_or_create(
                code=status_data['code'],
                defaults={'name': status_data['name']}
            )

        # Crear tipos de pago
        payment_types = [
            {'name': 'EFECTIVO', 'code': 'EFEC'},
        ]

        for payment_type_data in payment_types:
            PaymentType.objects.get_or_create(
                code=payment_type_data['code'],
                defaults={
                    'name': payment_type_data['name'],
                    'active': True
                }
            )
