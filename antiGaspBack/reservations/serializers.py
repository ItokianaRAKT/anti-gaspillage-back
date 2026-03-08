from rest_framework import serializers
from .models import Reservation
from products.models import Product

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation 
        fields = [
            'id_reservation',
            'quantity_reserved',
            'estimated_recovery_time',
            'date_reservation',
            'status_reservation',
            'product',
            'user'
        ]
        read_only_fields = [
            'id_reservation',
            'date_reservation',
            'status_reservation',
            'user'
        ]

    def validate(self, data):
        product = data['product']
        quantity = data['quantity_reserved']

        if quantity > product.current_stock:
            raise serializers.ValidationError(
                f"Stock insuffisant. Il ne reste que {product.current_stock} unité(s)"
            )
        return data