from django.contrib import admin
from .models import Pose


class PoseAdmin(admin.ModelAdmin):
    list_display = ("hip_y",)


admin.site.register(Pose, PoseAdmin)

# Register your models here.
