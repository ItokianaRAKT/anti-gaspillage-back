from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer, UserProfileSerializer, ChangePasswordSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Crée un nouveau compte utilisateur. Accessible sans authentification.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Génère directement les tokens après inscription
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Compte créé avec succès.",
            "user": UserProfileSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Blackliste le refresh token pour invalider la session.
    Requiert: { "refresh": "<token>" }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Le refresh token est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Déconnexion réussie."}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "Token invalide ou déjà blacklisté."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/auth/me/  → voir son profil
    PUT  /api/auth/me/  → modifier son profil (tous les champs)
    PATCH /api/auth/me/ → modifier partiellement
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """
    POST /api/auth/change-password/
    Requiert: { "old_password", "new_password", "new_password2" }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"old_password": "Mot de passe actuel incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"message": "Mot de passe modifié avec succès."}, status=status.HTTP_200_OK)