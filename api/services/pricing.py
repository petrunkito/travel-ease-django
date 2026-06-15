from django.db import transaction
from django.utils import timezone

from .models import PriceHistory


def get_active_price(service_type: str, service_id: int):
    return (
        PriceHistory.objects.filter(
            service_type=service_type,
            service_id=service_id,
            end_date__isnull=True,
        )
        .order_by('-start_date', '-id')
        .first()
    )


def list_service_prices(service_type: str, service_id: int):
    return PriceHistory.objects.filter(service_type=service_type, service_id=service_id).order_by('-start_date', '-id')


@transaction.atomic
def set_service_price(service_type: str, service_id: int, price, changed_at=None):
    changed_at = changed_at or timezone.now()

    active_price = get_active_price(service_type, service_id)
    if active_price:
        active_price.end_date = changed_at
        active_price.save(update_fields=['end_date'])

    return PriceHistory.objects.create(
        service_type=service_type,
        service_id=service_id,
        price=price,
        start_date=changed_at,
        end_date=None,
    )
