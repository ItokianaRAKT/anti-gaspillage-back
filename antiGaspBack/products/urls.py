from django.urls import path
from .views import ProductListView, ProductCreateView, ProductDetailView, ProductRelistView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<uuid:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<uuid:pk>/relist/', ProductRelistView.as_view(), name='product_relist'),
]