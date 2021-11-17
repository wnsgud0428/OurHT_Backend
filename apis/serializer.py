from django.db.models import fields
from rest_framework.serializers import ModelSerializer

# 로그인 인증을 위해
from rest_framework import serializers
from users import models as user_models
from exercises import models as exercise_models
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = ["id", "username", "password"]

        extra_kwargs = {
            "password": {"write_only": True, "required": True}
        }  # GET 했을때 비밀번호 안보여줌

    def create(self, validated_data):
        user = user_models.User.objects.create_user(**validated_data)
        Token.objects.create(user=user)  # 위에서 만들어진 user의 token create
        return user


class MotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = exercise_models.Motion
        fields = ["exercise", "count_number"]


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = exercise_models.Exercise
        fields = ["user", "created"]
