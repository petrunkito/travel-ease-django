from django.urls import path

from .views import FlightDetailAPIView, FlightListCreateAPIView

urlpatterns = [
    path('', FlightListCreateAPIView.as_view(), name='flights-list-create'),
    path('<int:flight_id>/', FlightDetailAPIView.as_view(), name='flights-detail'),
]
