from django.urls import include, path

urlpatterns = [
    path('departamentos/', include('api.catalogos.departamentos.urls')),
    path('municipios/', include('api.catalogos.municipios.urls')),
    path('type-transports/', include('api.catalogos.type_transport.urls')),
]
