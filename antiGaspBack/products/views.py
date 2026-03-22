from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializer import ProductSerializer, CreateProductSerializer
from .filters import ProductFilter


class ProductListView(generics.ListAPIView):
    """
    GET /api/products/
    Liste tous les produits disponibles et non expirés. Public.
    """
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True, current_stock__gt=0)
        return queryset.filter(
            id_product__in=[p.id_product for p in queryset if p.is_visible()]
        )


class ProductCreateView(APIView):
    """
    POST /api/products/create/
    Crée un produit. Requiert authentification.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateProductSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """
    GET    /api/products/<uuid:pk>/ → détail produit, public
    PATCH  /api/products/<uuid:pk>/ → modifier, réservé au propriétaire
    DELETE /api/products/<uuid:pk>/ → supprimer, réservé au propriétaire
    """
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.user != request.user:
            return Response({'error': 'Action non autorisée'}, status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductRelistView(APIView):
    """
    POST /api/products/<uuid:pk>/relist/
    Remet un produit en vente après non-récupération. Réservé au propriétaire.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.user != request.user:
            return Response({'error': 'Action non autorisée'}, status=status.HTTP_403_FORBIDDEN)
        product.is_available = True
        product.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)