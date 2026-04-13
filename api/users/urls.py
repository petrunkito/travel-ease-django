from django.urls import path

from .views import EmployeeCreateAPIView, LoginAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='users-login'),
    path('employees/', EmployeeCreateAPIView.as_view(), name='users-create-employee'),
]
