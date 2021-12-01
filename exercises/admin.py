from django.contrib import admin
from . import models


class MotionInline(admin.TabularInline):

    model = models.Motion


@admin.register(models.Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Exercise Admin Definition"""

    inlines = (MotionInline,)  # Exercise Admin에서 해당하는 Motion을 볼 수 있음

    list_display = (
        "pk",
        "user",
        "type",
        "created",
    )
    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "user",
                    "type",
                    "created",
                ),
            },
        ),
    )


@admin.register(models.Motion)
class MotionAdmin(admin.ModelAdmin):
    """Motion Admin Definition"""

    list_display = (
        "pk",
        "exercise",
        "count_number",
        "feedback_check",
    )

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "exercise",
                    "count_number",
                    "checklist",
                    "photo",
                    "feedback_check",
                ),
            },
        ),
    )
    filter_horizontal = ("checklist",)


@admin.register(models.Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    """Checklist Admin Definition"""

    list_display = ("check_item_name",)
