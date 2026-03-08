from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation

@receiver(post_save, sender=Reservation)
def decrement_stock(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.current_stock -= instance.quantity_reserved
        product.save()
        