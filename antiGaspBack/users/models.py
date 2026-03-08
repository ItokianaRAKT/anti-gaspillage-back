from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid
phone_validator = RegexValidator(    regex=r'^\+?\d{8,20}$',
    message="Numéro invalide. Format attendu: +261XXXXXXXX"
)
# Create your models here.
class User(AbstractUser):
    id_user=models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    tel1_user=models.CharField(max_length=20, 
        blank=True,
        null=True,
        validators=[phone_validator])
    tel2_user=models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[phone_validator])
    address_user=models.CharField(max_length=50)
    # chemin à modifier après (je sais pas c'est où)
    profile_pic_user=models.ImageField(
        blank=True,
        null=True,
        upload_to="users/profile_pics/"
    )
    saved_in_90_days=models.IntegerField(default=0)
    total_product_saved=models.IntegerField(default=0)

class UserBadge(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    badge=models.ForeignKey('badge.Badge', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'badge')