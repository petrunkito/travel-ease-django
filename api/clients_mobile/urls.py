from django.urls import path
from api.clients_mobile.views import PerfilClienteView, ReservasClienteView

urlpatterns = [
    path('perfil/', PerfilClienteView.as_view(), name='perfil-cliente'),
    path('reservas/', ReservasClienteView.as_view(), name='reservas-cliente'),
]