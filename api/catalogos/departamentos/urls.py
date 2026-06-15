from django.urls import path

from .views import DepartmentListCreateAPIView

urlpatterns = [
    path('', DepartmentListCreateAPIView.as_view(), name='departments-list-create'),
]
