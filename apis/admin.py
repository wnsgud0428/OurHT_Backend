from django.contrib import admin
from . import models
from .models import User
# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "username",
    )

    # list_display = [field.name for field in User._meta.get_fields()]