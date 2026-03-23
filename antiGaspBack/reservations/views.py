from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Reservation
from .serializers import ReservationSerializer

from badge.utils import assign_badges
from users.models import User

class ReservationCreateView(APIView):
    """
    POST /api/reservations/
    Crée une réservation. Requiert authentification.
    """
    permission_classes = []
#IsAuthenticated à ajouter





    def post(self, request):
#les deux prochaines lignes à supprimer
        user = User.objects.first()
        request.user = user
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyReservationsView(APIView):
    """GET /api/reservations/my/ — Mes réservations."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user).order_by('-date_reservation')
        return Response(ReservationSerializer(reservations, many=True).data)


class ReservationCollectView(APIView):
    """POST /api/reservations/<uuid>/collect/ — Marquer comme récupérée."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({'error': 'Réservation introuvable'}, status=status.HTTP_404_NOT_FOUND)

        if reservation.user != request.user:
            return Response({'error': 'Action non autorisée'}, status=status.HTTP_403_FORBIDDEN)

        if reservation.status_reservation != 'pending':
            return Response(
                {'error': f'Statut incompatible : "{reservation.status_reservation}"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.status_reservation = 'collected'
        reservation.save()

        # Mettre à jour les stats utilisateur
        user = request.user
        user.total_product_saved += reservation.quantity_reserved
        user.saved_in_90_days += reservation.quantity_reserved
        user.save()

        # Attribuer les badges mérités
        assign_badges(user)

        return Response(ReservationSerializer(reservation).data)


class ReservationNotCollectedView(APIView):

    """
    POST /api/reservations/<pk>/not-collected/
    Marque une réservation comme non récupérée et remet le stock.
    """
    permission_classes = []
# à remettre [IsAuthenticated]

    def post(self, request, pk):
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({'error': 'Réservation introuvable'}, status=status.HTTP_404_NOT_FOUND)

#        if reservation.user != request.user:
#            return Response({'error': 'Action non autorisée'}, status=status.HTTP_403_FORBIDDEN)


#        if reservation.status_reservation != 'pending':
#            return Response(
#                {'error': f'Impossible d\'annuler une réservation avec le statut "{reservation.status_reservation}"'},
#              status=status.HTTP_400_BAD_REQUEST
#           )



        product = reservation.product
        product.current_stock += reservation.quantity_reserved
        product.save()

        reservation.status_reservation = 'cancelled'
        reservation.save()

        return Response(ReservationSerializer(reservation).data)