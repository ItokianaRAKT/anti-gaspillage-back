from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer, CreateProductSerializer
from .filters import ProductFilter
from users.models import User

class ProductListView(generics.ListAPIView):
    """
    GET /api/products/
    Liste tous les produits disponibles et non expirés.
    Tri : gratuits en premier, puis par date de publication décroissante.
    Filtres : search, category, dlc_24h, is_free, lat+lng+distance_km
    """
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True, current_stock__gt=0)
        queryset = queryset.filter(
            id_product__in=[p.id_product for p in queryset if p.is_visible()]
        )
        # Priorité : gratuits en premier, puis plus récents
        return queryset.order_by('price_product', '-publication_date')


class ProductCreateView(APIView):

    """
    POST /api/products/create/
    Crée un produit. Requiert authentification.
    """
    permission_classes = []

    def post(self, request):
        from users.models import User
        user = User.objects.first()  # prend le premier user dispo, à supprimer après
        request.user = user          # à supprimer aussi
        # from users.models import User          # à décommenter
        # user = User.objects.first()            
        # request.user = user                   
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
    """
    GET    /api/products/<uuid>/ — public
    PATCH  /api/products/<uuid>/ — propriétaire uniquement
    DELETE /api/products/<uuid>/ — propriétaire uniquement
    """
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
    """POST /api/products/<uuid>/relist/ — Remettre en vente."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.user != request.user:
            return Response({'error': 'Action non autorisée'}, status=status.HTTP_403_FORBIDDEN)
        product.is_available = True
        product.save()
        return Response(ProductSerializer(product).data)