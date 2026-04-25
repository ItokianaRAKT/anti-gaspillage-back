from rest_framework import serializers
from .models import Product, PriceHistory
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.point import Point

PRICE_CAPS = {
    'pains et patisseries': 5000,
    'fruits et légumes': 8000,
    'plats faits maison': 15000,
    'invendus de commerçe': 20000,
}

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ('id_price_history', 'price_product', 'date_price_product')


class ProductSerializer(serializers.ModelSerializer):
    price_history = PriceHistorySerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name_category', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    is_expired = serializers.SerializerMethodField()
    is_free = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id_product', 'name_product', 'description_product',
            'price_product', 'initial_stock', 'current_stock',
            'expiration_date', 'publication_date',
            'recovery_address', 'recovery_time_limit',
            'is_available', 'image_product',
            'latitude', 'longitude',
            'category', 'category_name',
            'user', 'user_username',
            'price_history', 'is_expired', 'is_free',
        )

    def get_is_expired(self, obj):
        return obj.is_expired()

    def get_is_free(self, obj):
        return obj.is_free()


class CreateProductSerializer(serializers.ModelSerializer):
    description_product = serializers.CharField(required=False, allow_blank=True, default="")

    class Meta:
        model = Product
        fields = (
            'name_product', 'description_product',
            'price_product', 'initial_stock',
            'expiration_date', 'recovery_address', 'recovery_time_limit',
            'is_available', 'category', 'image_product',
            'latitude', 'longitude',
        )

    def validate(self, data):
        category = data.get('category')
        price = data.get('price_product', 0)

        if category:
            cat_name = category.name_category.lower()
            plafond = PRICE_CAPS.get(cat_name)
            if plafond and price > plafond:
                raise serializers.ValidationError({
                    'price_product': f'Prix trop élevé. Plafond pour cette catégorie : {plafond} Ar'
                })
        
        if price < 0:
            raise serializers.ValidationError({
                'price_product': 'Le prix ne peut pas être négatif.'
            })

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['current_stock'] = validated_data['initial_stock']
        
        try:
            geolocator = Nominatim(user_agent="antigasp")
            adresse_complete = validated_data.get('recovery_address', '')
            parties = [p.strip() for p in adresse_complete.split(',')]
            quartier = parties[-2] if len(parties) >= 2 else adresse_complete
            
            print(f"Géocodage de : {quartier}")
            location = geolocator.geocode(
                quartier,
                viewbox=[(47.4, -18.7), (47.7, -19.0)],
                bounded=True,
                timeout=10
            )
            print(f"Résultat : {location}")
            if location:
                validated_data['latitude'] = location.latitude
                validated_data['longitude'] = location.longitude
        except GeocoderTimedOut:
            print("Timeout géocodage")
        except Exception as e:
            print(f"Erreur géocodage : {e}")
        
        return Product.objects.create(user=user, **validated_data)