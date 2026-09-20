from django.urls import path
from api.clients_mobile.views import (
    PerfilClienteView,
    ReservasClienteView,
    SugerenciaClienteView,
    ValoracionClienteView,
)
from .views import MongoDBTestView

urlpatterns = [
    path('perfil/', PerfilClienteView.as_view(), name='perfil-cliente'),
    path('reservas/', ReservasClienteView.as_view(), name='reservas-cliente'),
    path('sugerencias/', SugerenciaClienteView.as_view(), name='sugerencias-cliente'),
    path('valoracion/', ValoracionClienteView.as_view(), name='valoracion-cliente'),
    path("test/",MongoDBTestView.as_view(),name="mongodb-test"),
]