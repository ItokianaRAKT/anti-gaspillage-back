from django.db import models
import uuid
from django.core.validators import MinValueValidator
from products.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()

class Reservation(models.Model):
    id_reservation=models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    quantity_reserved=models.IntegerField(validators=[MinValueValidator(1)])
    estimated_recovery_time=models.DateTimeField()
    date_reservation=models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('collected', 'Collected')
    ]
    status_reservation=models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending')
    product=models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
