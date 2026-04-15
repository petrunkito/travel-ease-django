from django.urls import path

from .views import TransportationDetailAPIView, TransportationListCreateAPIView

urlpatterns = [
    path('', TransportationListCreateAPIView.as_view(), name='transportation-list-create'),
    path('<int:transportation_id>/', TransportationDetailAPIView.as_view(), name='transportation-detail'),
]
