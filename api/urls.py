from django.urls import include, path

from .views import health_check

urlpatterns = [
    path('', health_check, name='health-check'),
    path('users/', include('api.users.urls')),
]
