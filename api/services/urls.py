from django.urls import include, path

urlpatterns = [
    path('flights/', include('api.services.flights.urls')),
    path('hotels/', include('api.services.hotels.urls')),
    path('transportation/', include('api.services.transportation.urls')),
]
