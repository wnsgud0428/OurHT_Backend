from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=10, default="")
    userid = models.CharField(max_length=20, default="")
    userpassword = models.CharField(max_length=20, default="")
    age = models.IntegerField(default="0", validators=[MinValueValidator(0), MaxValueValidator(99)])
    weight = models.IntegerField(default="0")
    gender = models.TextField(default="Not Selected Yet")

class Feedback(models.Model):
    pass