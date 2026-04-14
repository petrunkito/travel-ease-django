from django.urls import include, path

urlpatterns = [
    path('departamentos/', include('api.catalogos.departamentos.urls')),
    path('municipios/', include('api.catalogos.municipios.urls')),
]
