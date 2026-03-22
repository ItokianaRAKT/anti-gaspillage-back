from rest_framework import serializers
from .models import Badge
from users.models import UserBadge


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id_badge', 'name_badge', 'badge_type', 'picture_badge', 'obtaining_alone_badge')


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = ('badge',)