from django.urls import path
from .views import RegisterView, LogoutView, ProfileView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('me/', ProfileView.as_view(), name='auth_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='auth_change_password'),
]