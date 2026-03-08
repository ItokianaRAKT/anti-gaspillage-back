from django.urls import path
from .views import ReservationCreateView, ReservationNonRecoveredView

urlpatterns = [
    path('', ReservationCreateView.as_view(), name='reservation-create'),
    path('<uuid:pk>/non-recovered/', ReservationNonRecoveredView.as_view(), name='reservation-non-recovered')
]