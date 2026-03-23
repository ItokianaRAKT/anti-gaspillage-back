from django.db import models
import uuid

class Badge(models.Model):
    BRONZE = 'bronze'
    SILVER = 'silver'
    GOLD   = 'gold'

    BADGE_TYPES = [
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
        (GOLD,   'Gold'),
    ]

    # Seuils de produits sauvés pour obtenir chaque badge
    THRESHOLDS = {
        BRONZE: 5,
        SILVER: 20,
        GOLD:   50,
    }

    id_badge = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_badge = models.CharField(max_length=100)
    badge_type = models.CharField(max_length=10, choices=BADGE_TYPES, unique=True, default='bronze')
    picture_badge = models.ImageField(upload_to='badges/')
    obtaining_alone_badge = models.IntegerField(help_text="Nombre de produits sauvés requis")

    def __str__(self):
        return self.name_badge