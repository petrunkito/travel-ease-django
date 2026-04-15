from django.urls import path

from .views import HotelDetailAPIView, HotelListCreateAPIView

urlpatterns = [
    path('', HotelListCreateAPIView.as_view(), name='hotels-list-create'),
    path('<int:hotel_id>/', HotelDetailAPIView.as_view(), name='hotels-detail'),
]
