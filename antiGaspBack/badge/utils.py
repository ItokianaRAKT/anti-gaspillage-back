from .models import Badge
from users.models import UserBadge


def assign_badges(user):
    """
    Vérifie et attribue automatiquement les badges mérités
    selon total_product_saved de l'utilisateur.
    Appelé après chaque collecte de réservation.
    """
    for badge in Badge.objects.all():
        if user.total_product_saved >= badge.obtaining_alone_badge:
            UserBadge.objects.get_or_create(user=user, badge=badge)