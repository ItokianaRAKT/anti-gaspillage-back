from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from reservations.models import Reservation


class CommunityStatsView(APIView):
    """
    GET /api/stats/
    Retourne les statistiques globales de la communauté.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        collected = Reservation.objects.filter(status_reservation='collected')

        total_saved = sum(r.quantity_reserved for r in collected)

        since_90_days = timezone.now() - timedelta(days=90)
        saved_90_days = sum(
            r.quantity_reserved for r in collected
            if r.date_reservation >= since_90_days
        )

        return Response({
            "total_saved": total_saved,
            "saved_last_90_days": saved_90_days,
        })