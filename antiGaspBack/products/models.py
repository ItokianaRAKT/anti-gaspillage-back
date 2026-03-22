from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid

# Plafond de prix configurable
PRICE_CAP = 50000  # exemple Ariary

class Product(models.Model):
    id_product = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name_product = models.CharField(max_length=200)
    description_product = models.TextField()
    price_product = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0),              # ← autorise 0 (gratuit)
            MaxValueValidator(PRICE_CAP),      # ← plafond de prix
        ]
    )
    initial_stock = models.IntegerField(validators=[MinValueValidator(1)])
    current_stock = models.IntegerField()
    expiration_date = models.DateField()
    publication_date = models.DateTimeField(auto_now_add=True)
    recovery_address = models.CharField(max_length=200)
    recovery_time_limit = models.DateTimeField()
    is_available = models.BooleanField(default=True)

    # Coordonnées GPS pour la carte et le filtre distance
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        'category.Category',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    image_product = models.ImageField(
        upload_to='product/',
        blank=True,
        null=True
    )

    def is_expired(self):
        return self.expiration_date < timezone.localdate()

    def is_visible(self):
        return self.is_available and not self.is_expired()

    def is_free(self):
        return self.price_product == 0


class PriceHistory(models.Model):
    id_price_history = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    price_product = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    date_price_product = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='price_history'
    )