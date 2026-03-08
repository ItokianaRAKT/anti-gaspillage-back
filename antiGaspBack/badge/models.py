from django.db import models
import uuid
# Create your models here.
class Badge(models.Model):
    id_badge=models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    name_badge=models.CharField(max_length=100)
    picture_badge=models.ImageField(upload_to="products/")
    obtaining_alone_badge=models.IntegerField()

    
