from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Reservation
from .serializers import ReservationSerializer
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()

class ReservationCreateView(APIView):
    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(pk="02609020-9dbf-4212-bfde-46b7600814ef")
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReservationNonRecoveredView(APIView):
    def patch(self, request, pk):
        try:
            reservation =  Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({'error': 'Réservation introuvable'}, status=status.HTTP_404_NOT_FOUND)
        
        product = reservation.product
        product.current_stock += reservation.quantity_reserved
        product.save()

        reservation.status_reservation = 'cancelled'
        reservation.save()

        return Response({'message': 'Réservation non récupérée'}, status=status.HTTP_200_OK)