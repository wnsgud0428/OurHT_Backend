from django.db import models


class Exercise(models.Model):
    """Exercise Model Definition"""

    TYPE_SQUAT = "squat"
    TYPE_PUSHUP = "pushup"
    TYPE_PLANK = "plank"

    TYPE_CHOICES = (
        (TYPE_SQUAT, "Squat"),
        (TYPE_PUSHUP, "Pushup"),
        (TYPE_PLANK, "Plank"),
    )

    user = models.ForeignKey(
        "users.User", related_name="exercises", on_delete=models.CASCADE, null=True
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=False, null=True)
    # 원래는 auto_now_add를 True로 해야됨.
    # admin페이지에서 add하여 테스트하기 위해 False로 해놓음.
    count_number = models.IntegerField(null=True)
    checklist = models.ManyToManyField(
        "Checklist", related_name="exercises", blank=True
    )

    def __str__(self):
        return f"{self.user} - {self.type} - {self.created} - {self.count_number}/10"


class Photo(models.Model):  # rooms앱 -> Photo모델 참고
    """Photo Model Definition"""

    file = models.ImageField()
    exercise = models.ForeignKey(
        "Exercise", related_name="photos", on_delete=models.CASCADE
    )


class Checklist(models.Model):  # rooms앱 -> Amenity앱 참고
    """Checklist Model Definition"""

    check_item_name = models.CharField(
        max_length=300
    )  # 한글로 입력할거라 max_length설정 다시 해야될수도

    def __str__(self):
        return self.check_item_name
