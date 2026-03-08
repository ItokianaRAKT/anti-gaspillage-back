from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id_review', 'rating_review', 'comment_review', 'date_review', 'product', 'user']
        read_only_fields = ['id_review', 'date_review', 'user']
        