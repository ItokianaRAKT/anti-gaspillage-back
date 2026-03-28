from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer, CreateProductSerializer
from .filters import ProductFilter

from reservations.models import Reservation
from reservations.serializers import ReservationSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True, current_stock__gt=0)
        queryset = queryset.filter(
            id_product__in=[p.id_product for p in queryset if p.is_visible()]
        )
        return queryset.order_by('price_product', '-publication_date')


class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from users.models import User
        from users.models import User          
        user = User.objects.first()            
        request.user = user                   
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
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return Response(ProductSerializer(product).data)

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.user != request.user:
            return Response({'error': 'Action non autorisée'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CreateProductSerializer(
            product, data=request.data, partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.user != request.user:
            return Response({'error': 'Action non autorisée'}, status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductRelistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.user != request.user:
            return Response({'error': 'Action non autorisée'}, status=status.HTTP_403_FORBIDDEN)
        product.is_available = True
        product.save()
        return Response(ProductSerializer(product).data)


class MyProductsView(generics.ListAPIView):
    """
    GET /api/products/my/
    Liste des produits publiés par l'utilisateur connecté,
    avec les réservations associées.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        produits = Product.objects.filter(user=request.user).order_by('-publication_date')
        result = []
        for product in produits:
            product_data = ProductSerializer(product).data
            reservations = Reservation.objects.filter(
                product=product,
                status_reservation__in=['pending', 'confirmed', 'collected']
            ).select_related('user')
            product_data['reservations'] = ReservationSerializer(reservations, many=True).data
            result.append(product_data)
        return Response(result)