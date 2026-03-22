from django.urls import path
from .views import UserBadgesView

urlpatterns = [
    path('users/<uuid:pk>/badges/', UserBadgesView.as_view(), name='user_badges'),
]