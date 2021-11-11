from django.contrib import admin
from . import models


@admin.register(models.Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Exercise Admin Definition"""

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

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "exercise",
                    "count_number",
                    "checklist",
                    "photo",
                ),
            },
        ),
    )
    filter_horizontal = ("checklist",)


@admin.register(models.Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    """Checklist Admin Definition"""

    list_display = ("check_item_name",)
