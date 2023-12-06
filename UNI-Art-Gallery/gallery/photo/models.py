from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class library(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    image = CloudinaryField('image')

    def __str__(self) -> str:
        return self.title