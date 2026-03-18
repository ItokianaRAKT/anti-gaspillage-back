from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),
    path('api/reservations/', include('reservations.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/categories/', include('category.urls')),

    # Auth
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('users.urls')),  # register, logout, me, change-password
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
