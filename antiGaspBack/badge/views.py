from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from users.models import User, UserBadge
from .serializers import UserBadgeSerializer


class UserBadgesView(APIView):
    """
    GET /api/users/<uuid>/badges/
    Retourne les badges obtenus par un utilisateur.
    """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user_badges = UserBadge.objects.filter(user=user).select_related('badge')
        serializer = UserBadgeSerializer(user_badges, many=True)
        return Response(serializer.data)