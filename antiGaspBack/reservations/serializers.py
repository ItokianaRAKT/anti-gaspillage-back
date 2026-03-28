from rest_framework import serializers
from .models import Reservation


class ReservateurSerializer(serializers.Serializer):
    """Infos publiques de l'user qui a réservé"""
    id_user = serializers.UUIDField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    tel1_user = serializers.CharField()
    tel2_user = serializers.CharField()
    address_user = serializers.CharField()


class ReservationSerializer(serializers.ModelSerializer):
    reservateur = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            'id_reservation',
            'quantity_reserved',
            'estimated_recovery_time',
            'date_reservation',
            'status_reservation',
            'product',
            'user',
            'reservateur',
        ]
        read_only_fields = [
            'id_reservation',
            'date_reservation',
            'status_reservation',
            'user',
            'reservateur',
        ]

    def get_reservateur(self, obj):
        u = obj.user
        return {
            "id_user": str(u.id_user),
            "username": u.username,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "email": u.email,
            "tel1_user": u.tel1_user or "",
            "tel2_user": u.tel2_user or "",
            "address_user": u.address_user or "",
        }

    def validate(self, data):
        product = data['product']
        quantity = data['quantity_reserved']
        if quantity > product.current_stock:
            raise serializers.ValidationError(
                f"Stock insuffisant. Il ne reste que {product.current_stock} unité(s)"
            )
        return data