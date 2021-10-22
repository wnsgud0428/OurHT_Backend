from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from .models import Feedback, Photo, User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'userid', 'age', 'weight', 'gender',)

class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = ()

class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = ()