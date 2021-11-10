from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from users import models as user_models


class UserSerializer(ModelSerializer):
    class Meta:
        model = user_models.User
        fields = ()
