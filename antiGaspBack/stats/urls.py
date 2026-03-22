from django.urls import path
from .views import CommunityStatsView

urlpatterns = [
    path('', CommunityStatsView.as_view(), name='community_stats'),
]