from rest_framework import serializers
from .models import Product, PriceHistory


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ('id_price_history', 'price_product', 'date_price_product')


class ProductSerializer(serializers.ModelSerializer):
    price_history = PriceHistorySerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name_category', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id_product', 'name_product', 'description_product',
            'price_product', 'initial_stock', 'current_stock',
            'expiration_date', 'publication_date',
            'recovery_address', 'recovery_time_limit',
            'is_available', 'image_product',
            'category', 'category_name',
            'user', 'user_username',
            'price_history', 'is_expired',
        )

    def get_is_expired(self, obj):
        return obj.is_expired()


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name_product', 'description_product',
            'price_product', 'initial_stock',
            'expiration_date', 'recovery_address', 'recovery_time_limit',
            'is_available', 'category', 'image_product',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['current_stock'] = validated_data['initial_stock']
        return Product.objects.create(user=user, **validated_data)