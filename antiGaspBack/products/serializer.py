from rest_framework import serializers
from .models import Product
from django.contrib.auth import get_user_model
User = get_user_model
from category.models import Category

class ProductSerializer(serializers.ModelSerializer):
    is_expired=serializers.SerializerMethodField()
    is_visible=serializers.SerializerMethodField()
    price_product = serializers.FloatField()
    class Meta:

        model = Product
        fields = [
            'id_product',
            'name_product',
            'description_product',
            'price_product',
            'initial_stock',
            'current_stock',
            'expiration_date',
            'publication_date',
            'recovery_address',
            'recovery_time_limit',
            'category',
            'user',
            'is_expired',
            'is_visible',
            'is_available',
            'image_product',
        ]
        read_only_fields = [
            'publication_date',
            'user'
        ]

    def get_is_expired(self, obj):
        return obj.is_expired()

    def get_is_visible(self, obj):
        return obj.is_visible()

class CreateProductSerializer(serializers.ModelSerializer):
    description_product=serializers.CharField(required=False, allow_blank=True, default="")
    class Meta:
        model = Product
        fields = [
            'id_product',
            'name_product',
            'description_product',
            'price_product',
            'initial_stock',
            'expiration_date',
            'recovery_address',
            'recovery_time_limit',
            'category',
            'image_product',
        ]

    def create(self, validated_data):
        validated_data['current_stock'] = validated_data['initial_stock']
        request = self.context.get('request')
        if request:
            validated_data['user'] = request.user
        return Product.objects.create(**validated_data)