from django.urls import path
from .views import (
    ReservationCreateView,
    MyReservationsView,
    ReservationCollectView,
    ReservationNotCollectedView,
)

urlpatterns = [
    path('', ReservationCreateView.as_view(), name='reservation_create'),
    path('my/', MyReservationsView.as_view(), name='my_reservations'),
    path('<uuid:pk>/collect/', ReservationCollectView.as_view(), name='reservation_collect'),
    path('<uuid:pk>/not-collected/', ReservationNotCollectedView.as_view(), name='reservation_not_collected'),
]