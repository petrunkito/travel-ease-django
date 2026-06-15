from django.urls import path

from .views import TouristPackageDetailAPIView, TouristPackageListCreateAPIView

urlpatterns = [
    path('', TouristPackageListCreateAPIView.as_view(), name='tourist-packages-list-create'),
    path('<int:package_id>/', TouristPackageDetailAPIView.as_view(), name='tourist-packages-detail'),
]
