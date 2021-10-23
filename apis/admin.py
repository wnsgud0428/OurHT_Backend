from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "username",
        "userid",
        "userpassword",
        "age",
        "weight",
        "gender",
    )
    

@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = ()

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    list_display = ()