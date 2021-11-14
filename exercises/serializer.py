from rest_framework.serializers import ModelSerializer
from exercises import models as exercise_models

class ExerciseSerializer(ModelSerializer):
    class Meta:
        model = exercise_models.Exercise
        fields = ()

class MotionSerializer(ModelSerializer):
    class Meta:
        model = exercise_models.Motion
        fields = ()

class ChecklistSerializer(ModelSerializer):
    class Meta:
        model = exercise_models.Checklist
        fields = ()