from django.urls import path
from api.clients_mobile.views import PerfilClienteView

urlpatterns = [
    path('perfil/', PerfilClienteView.as_view(), name='perfil-cliente'),
]