from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReservationViewSet, PaymentTypeViewSet,
    ReservationStatusViewSet
)

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'payment-types', PaymentTypeViewSet, basename='payment-type')
router.register(r'reservation-statuses', ReservationStatusViewSet, basename='reservation-status')

app_name = 'reservations'

urlpatterns = [
    path('', include(router.urls)),
]
