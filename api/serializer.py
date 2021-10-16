from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from .models import Image, User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'