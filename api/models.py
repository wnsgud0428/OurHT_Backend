from django.db import models
from django.db.models.base import Model

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=10)

class Image(models.Model):
    pass

