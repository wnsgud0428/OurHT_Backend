from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        #"age",
        #"weight",
        #"gender",
    )

@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):

    list_display = (
        "image_url",
    )