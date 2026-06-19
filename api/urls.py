from django.urls import include, path

from .views import (
    health_check,
    warehouse_high_season,
    warehouse_income_by_destination,
    warehouse_top_clients,
    warehouse_top_packages,
)

urlpatterns = [
    path('', health_check, name='health-check'),
    path('warehouse/ingresos-por-destino/', warehouse_income_by_destination, name='warehouse-income-by-destination'),
    path('warehouse/top-clientes/', warehouse_top_clients, name='warehouse-top-clients'),
    path('warehouse/paquetes-mas-vendidos/', warehouse_top_packages, name='warehouse-top-packages'),
    path('warehouse/temporada-alta/', warehouse_high_season, name='warehouse-high-season'),
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
