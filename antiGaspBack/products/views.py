from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from .models import Product
from .serializer import ProductSerializer, CreateProductSerializer
from .filters import ProductFilter
from users.models import User
# Create your views here.
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True, current_stock__gt=0)
        return queryset.filter(
        id_product__in=[p.id_product for p in queryset if p.is_visible()]
    )
    
class ProductCreateView(APIView):
    def post(self, request):
        user = User.objects.get(pk="02609020-9dbf-4212-bfde-46b7600814ef")
        request.user = user
        print(request.FILES)
        serializer = CreateProductSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetailView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)