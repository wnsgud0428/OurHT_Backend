from django.db.models.fields import CharField
from rest_framework.serializers import ModelSerializer
from apis import serializer
from exercises import models as exercise_models


class ExerciseSerializer(ModelSerializer):
    class Meta:
        model = exercise_models.Exercise
        fields = "__all__"


class ChecklistSerializer(ModelSerializer):
    class Meta:
        model = exercise_models.Checklist
        fields = ("pk",)


class MotionSerializer(ModelSerializer):
    checklist = ChecklistSerializer(read_only=True, many=True)

    class Meta:
        model = exercise_models.Motion
        fields = "__all__"
