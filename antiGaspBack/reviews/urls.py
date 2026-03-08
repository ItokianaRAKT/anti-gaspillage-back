from django.urls import path
from .views import ReviewCreateView, ProductReviewsView

urlpatterns = [
    path('', ReviewCreateView.as_view(), name='review-create'),
    path('product/<uuid:product_id>/', ProductReviewsView.as_view(), name='product_reviews'),
]