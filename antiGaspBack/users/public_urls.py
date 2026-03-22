from django.urls import path
from .views import UserPublicProfileView, UserStatsView

urlpatterns = [
    path('<uuid:pk>/profile/', UserPublicProfileView.as_view(), name='user_public_profile'),
    path('<uuid:pk>/stats/', UserStatsView.as_view(), name='user_stats'),
]