from django.urls import include, path

from .views import health_check

urlpatterns = [
    path('', health_check, name='health-check'),
    path('users/', include('api.users.urls')),
    path('municipios/', include('api.catalogos.municipios.urls')),
    path('catalogos/', include('api.catalogos.urls')),
    path('services/', include('api.services.urls')),
    path('packages/', include('api.packages.urls')),
    path('paquetes/', include('api.packages.urls')),
    path('clientes/', include('api.clients.urls')),
    path('clients/', include('api.clients.urls')),
    path('reservations/', include(('api.reservations.urls', 'reservations'), namespace='reservations')),
    path('reservas/', include(('api.reservations.urls', 'reservations'), namespace='reservas')),
]
