from django.urls import path

from .views import MunicipalityByDepartmentAPIView, MunicipalityListCreateAPIView

urlpatterns = [
    path('', MunicipalityListCreateAPIView.as_view(), name='municipalities-list-create'),
    path('departamento/<int:department_id>/', MunicipalityByDepartmentAPIView.as_view(), name='municipalities-by-department'),
]
