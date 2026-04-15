from django.urls import path

from .views import TypeTransportDetailAPIView, TypeTransportListCreateAPIView

urlpatterns = [
    path('', TypeTransportListCreateAPIView.as_view(), name='type-transports-list-create'),
    path('<int:type_transport_id>/', TypeTransportDetailAPIView.as_view(), name='type-transports-detail'),
]
