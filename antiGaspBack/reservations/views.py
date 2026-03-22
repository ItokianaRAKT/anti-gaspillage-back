from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Reservation
from .serializers import ReservationSerializer


class ReservationCreateView(APIView):
    """
    POST /api/reservations/
    Crée une réservation. Requiert authentification.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyReservationsView(APIView):
    """
    GET /api/reservations/my/
    Liste les réservations de l'utilisateur connecté.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user).order_by('-date_reservation')
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReservationCollectView(APIView):
    """
    POST /api/reservations/<pk>/collect/
    Marque une réservation comme récupérée.
    """
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
                {'error': f'Impossible de collecter une réservation avec le statut "{reservation.status_reservation}"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.status_reservation = 'collected'
        reservation.save()

        # Mettre à jour les stats de l'utilisateur
        user = request.user
        user.total_product_saved += reservation.quantity_reserved
        user.saved_in_90_days += reservation.quantity_reserved
        user.save()

        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReservationNotCollectedView(APIView):
    """
    POST /api/reservations/<pk>/not-collected/
    Marque une réservation comme non récupérée et remet le stock.
    """
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
                {'error': f'Impossible d\'annuler une réservation avec le statut "{reservation.status_reservation}"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Remettre le stock
        product = reservation.product
        product.current_stock += reservation.quantity_reserved
        product.save()

        reservation.status_reservation = 'cancelled'
        reservation.save()

        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)