from django.urls import path

from .views import TransportationDetailAPIView, TransportationListCreateAPIView, TransportationPriceListCreateAPIView

urlpatterns = [
    path('', TransportationListCreateAPIView.as_view(), name='transportation-list-create'),
    path('<int:transportation_id>/', TransportationDetailAPIView.as_view(), name='transportation-detail'),
    path('<int:transportation_id>/prices/', TransportationPriceListCreateAPIView.as_view(), name='transportation-prices'),
]
