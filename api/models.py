from django.db import models
from django.db.models.base import Model

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField()

class Image(models.Model):
    name = models.CharField(max_length=10)
    image_data = models.ImageField(upload_to="")

