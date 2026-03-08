from django.db import models
import uuid
# Create your models here.
class Category(models.Model):
    id_category=models.UUIDField( 
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    name_category=models.CharField(max_length=20)