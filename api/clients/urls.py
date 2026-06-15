from django.urls import path

from .views import ClientDetailAPIView, ClientListCreateAPIView

urlpatterns = [
    path('', ClientListCreateAPIView.as_view(), name='clients-list-create'),
    path('<int:client_id>/', ClientDetailAPIView.as_view(), name='clients-detail'),
]
