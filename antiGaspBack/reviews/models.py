from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    id_review=models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    rating_review=models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment_review=models.CharField(max_length=500)
    date_review=models.DateTimeField(auto_now_add=True)
    product=models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE
        )
    user=models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
        )