from decimal import Decimal

from django.db.models import Model

from api.services.flights.models import Flight
from api.services.hotels.models import Hotel
from api.services.models import PriceHistory
from api.services.pricing import get_active_price
from api.services.transportation.models import Transportation

from .models import PackageDetail

SERVICE_MODEL_MAP = {
    PriceHistory.ServiceType.FLIGHT: Flight,
    PriceHistory.ServiceType.HOTEL: Hotel,
    PriceHistory.ServiceType.TRANSPORTATION: Transportation,
}

SERVICE_GROUP_KEY_MAP = {
    PriceHistory.ServiceType.FLIGHT: 'flights',
    PriceHistory.ServiceType.HOTEL: 'hotels',
    PriceHistory.ServiceType.TRANSPORTATION: 'transportation',
}


def normalize_service_type(service_type: str) -> str:
    if service_type not in SERVICE_MODEL_MAP:
        raise ValueError('Tipo de servicio invalido.')
    return service_type


def get_service_instance(service_type: str, service_id: int) -> Model | None:
    model_class = SERVICE_MODEL_MAP.get(service_type)
    if not model_class:
        return None

    queryset = model_class.objects.all()
    if service_type == PriceHistory.ServiceType.TRANSPORTATION:
        queryset = queryset.select_related('type_transport')

    try:
        return queryset.get(pk=service_id)
    except model_class.DoesNotExist:
        return None


def get_service_snapshot(service_type: str, service_id: int) -> dict:
    service = get_service_instance(service_type, service_id)
    if not service:
        return {}

    if service_type == PriceHistory.ServiceType.FLIGHT:
        return {
            'id': service.id,
            'airline': service.airline,
            'origin': service.origin,
            'destination': service.destination,
            'departure_date': service.departure_date,
            'arrival_date': service.arrival_date,
            'active': service.active,
        }

    if service_type == PriceHistory.ServiceType.HOTEL:
        return {
            'id': service.id,
            'name': service.name,
            'city': service.city,
            'stars': service.stars,
            'category': service.category,
            'active': service.active,
        }

    if service_type == PriceHistory.ServiceType.TRANSPORTATION:
        return {
            'id': service.id,
            'origin': service.origin,
            'destination': service.destination,
            'type_transport': {
                'id': service.type_transport_id,
                'name': service.type_transport.name,
                'code': service.type_transport.code,
            },
            'active': service.active,
        }

    return {}


def get_service_unit_price(service_type: str, service_id: int):
    price_row = get_active_price(service_type, service_id)
    return price_row.price if price_row else None


def calculate_detail_total(quantity: int, unit_price: Decimal) -> Decimal:
    return (Decimal(quantity) * unit_price).quantize(Decimal('0.01'))


def serialize_package_detail(detail: PackageDetail) -> dict:
    return {
        'id': detail.id,
        'service_type': detail.service_type,
        'service_id': detail.service_id,
        'quantity': detail.quantity,
        'unit_price': detail.unit_price,
        'total': detail.total,
        'service': get_service_snapshot(detail.service_type, detail.service_id),
    }
