from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
# Create your models here.

# 유저 모델 정의
class User(models.Model):
    username = models.CharField(max_length=10)
    userid = models.CharField(max_length=20, default="")
    userpassword = models.CharField(max_length=20, default="")
    age = models.IntegerField(default="0", validators=[MinValueValidator(0), MaxValueValidator(99)])
    weight = models.IntegerField(default="0")
    gender = models.TextField(default="Not Selected Yet")

# 운동 피드백 모델 정의
class Feedback(models.Model):
    user = models.ForeignKey("User", related_name="feedbacks", on_delete=models.CASCADE, default=False)
    categori = models.CharField(max_length=10, default="")
    day = models.DateTimeField("date created", default=datetime.datetime.now)
    result = models.IntegerField(default="0")
    count = models.IntegerField(default="0")

# 운동 사진 정의
class Photo(models.Model):
    caption = models.CharField(max_length=80)
    # /photos 폴더에 저장
    file = models.ImageField(upload_to="photos")
    feedback = models.ForeignKey("Feedback", related_name="photos", on_delete=models.CASCADE)