from django.db import models
from django.db.models.base import Model

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    weight = models.IntegerField()
    gender = models.CharField()

class Image(models.Model):
    user = models.ForeignKey("User", related_name="Image", on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    image_data = models.ImageField(upload_to="")

class Calendar(models.Model):
    user = models.ForeignKey("User", related_name="Calendar", on_delete=models.CASCADE)

class Sport(models.Model):
    pass
