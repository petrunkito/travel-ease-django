from django.urls import path

from .views import MunicipalityListCreateAPIView

urlpatterns = [
    path('', MunicipalityListCreateAPIView.as_view(), name='municipalities-list-create'),
]
